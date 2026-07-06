from crewai.flow.flow import Flow, start, listen, router
from pydantic import BaseModel
from the_roadmapper.crew import TheRoadmapper
import json


class RoadmapState(BaseModel):
    topic: str = ""

    analysis_output: str = ""
    resources_output: str = ""

    roadmap_output: str = ""
    review_output: str = ""

    revision_notes: str = ""

    revision_count: int = 0
    max_revisions: int = 4


class RoadmapFlow(Flow[RoadmapState]):

    

    def _research(self):
        crew = TheRoadmapper().research_crew()

        crew.kickoff(
            inputs={
                "topic": self.state.topic,
                
            }
        )

        self.state.analysis_output = crew.tasks[0].output.raw
        self.state.resources_output = crew.tasks[2].output.raw


    def _assembly(self):
        crew = TheRoadmapper().assembly_crew()

        crew.kickoff(
            inputs={
                "topic": self.state.topic,
                "resources_output": self.state.resources_output,
                
            }
        )

        self.state.roadmap_output = crew.tasks[0].output.raw
        self.state.review_output = crew.tasks[1].output.raw


    def _edit(self):
        crew = TheRoadmapper().editor_crew()

        crew.kickoff(
            inputs={
                "topic": self.state.topic,
                "roadmap_output": self.state.roadmap_output,
                "revision_notes": self.state.revision_notes,
            }
        )

        self.state.roadmap_output = crew.tasks[0].output.raw


    def _review_revision(self):
        crew = TheRoadmapper().review_crew()

        crew.kickoff(
            inputs={
                "topic": self.state.topic,
                "roadmap_output": self.state.roadmap_output,
                "revision_notes": self.state.revision_notes,
            }
        )

        self.state.review_output = crew.tasks[0].output.raw


    @start()
    def run_research(self):
        self._research()


    @listen(run_research)
    def run_assembly(self):
        self._assembly()


   
    @router(run_assembly)
    def check_review(self):

        try:
            review = json.loads(self.state.review_output)

        except json.JSONDecodeError:
            print("Reviewer returned invalid JSON.")
            return "failed"

        status = review.get("status")

        if status == "approved":
            self.state.revision_notes = json.dumps([], indent=2)
            return "approved"

        if status == "needs_revision":
            self.state.revision_notes = json.dumps(
                review.get("issues", []),
                indent=2
            )

            self.state.revision_count += 1

            if self.state.revision_count > self.state.max_revisions:
                return "failed"

            return "needs_revision"

        return "failed"


    @listen("needs_revision")
    def rerun_editor(self):

        while True:

            self._edit()
            self._review_revision()

            route = self.check_review()

            if route == "approved":
                self.finish()
                break

            elif route == "failed":
                self.failed_execution()
                break

            # if route == "needs_revision"
            # continue loop

           
    @listen("approved")
    def finish(self):

        print("\n========== ROADMAP APPROVED ==========\n")
        print(self.state.roadmap_output)


    @listen("failed")
    def failed_execution(self):

        print("\n========== FLOW FAILED ==========\n")
        print(f"Revision Attempts : {self.state.revision_count}")

        print("\nReviewer Output:\n")
        print(self.state.review_output)