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
    max_revisions: int = 3


class RoadmapFlow(Flow[RoadmapState]):

    def _assembly(self):
        crew = TheRoadmapper().assembly_crew()

        crew.kickoff(
            inputs={
                "topic": self.state.topic,
                "analysis_output": self.state.analysis_output,
                "resources_output": self.state.resources_output,
                "revision_notes": self.state.revision_notes,
            }
        )

        self.state.roadmap_output = crew.tasks[0].output.raw
        self.state.review_output = crew.tasks[1].output.raw

    @start()
    def run_research(self):

        crew = TheRoadmapper().research_crew()

        crew.kickoff(
            inputs={
                "topic": self.state.topic
            }
        )

        self.state.analysis_output = crew.tasks[0].output.raw
        self.state.resources_output = crew.tasks[2].output.raw


    
    @listen(run_research)
    def run_assembly(self):
        self._assembly()


    @listen("revise")
    def revise_assembly(self):
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
            return "approved"

        if status == "needs_revision":

            self.state.revision_count += 1

            if self.state.revision_count >= self.state.max_revisions:
                return "failed"

            self.state.revision_notes = json.dumps(
                review.get("issues", []),
                indent=2
            )

            return "revise"

        return "failed"
    @listen("revise")
    def revise_assembly(self):
        self._assembly()
        # manually re-route
        route = self.check_review()
        if route == "approved":
            self.finish()
        elif route == "failed":
            self.failed_execution()
        elif route == "revise":
            self.revise_assembly()

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