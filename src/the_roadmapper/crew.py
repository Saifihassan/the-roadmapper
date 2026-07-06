from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field

from crewai import  LLM
import os

from typing import List, Literal
class AnalysisLevel(BaseModel):
    description: str
    estimated_weeks: int = Field(ge=1, le=52)
    concepts: List[str] = Field(min_length=4, max_length=10)
class AnalysisOutput(BaseModel):
    beginner: AnalysisLevel
    intermediate: AnalysisLevel
    advanced: AnalysisLevel

class QueryLevel(BaseModel):
    queries: List[str]


class QueryOutput(BaseModel):
    beginner: QueryLevel
    intermediate: QueryLevel
    advanced: QueryLevel


class Resource(BaseModel):
    title: str
    url: str
    type: Literal[
        "video",
        "article",
        "course",
        "documentation",
        "book"
    ]


class ResourceConcept(BaseModel):
    name: str
    resources: List[Resource] = Field(min_length=1, max_length=3)


class ResourceLevel(BaseModel):
    concepts: List[ResourceConcept]


class ResourceOutput(BaseModel):
    beginner: ResourceLevel
    intermediate: ResourceLevel
    advanced: ResourceLevel



class Concept(BaseModel):
    name: str

    resources: List[Resource] = Field(min_length=1, max_length=5)

    completed: bool = False

    difficulty: Literal["Easy", "Medium", "Hard"]

    priority: Literal["Must-do", "Optional"]


class RoadmapLevel(BaseModel):
    description: str

    estimated_weeks: int = Field(ge=1, le=52)

    concepts: List[Concept] = Field(min_length=4, max_length=10)


class Roadmap(BaseModel):
    beginner: RoadmapLevel
    intermediate: RoadmapLevel
    advanced: RoadmapLevel


class ReviewIssue(BaseModel):
    type: Literal[
        "missing_concepts",
        "missing_resources",
        "duplicate_resources",
        "incorrect_order",
        "incorrect_difficulty",
        "incorrect_priority",
        "formatting",
        "invalid_json"
    ]

    description: str


class ReviewOutput(BaseModel):
    status: Literal[
        "approved",
        "needs_revision"
    ]

    issues: List[ReviewIssue] = []

gpt4o = LLM(  # analyze
    model="gpt-4o",
    api_key=os.getenv("BLUESMIND_API_KEY"),
    base_url=os.getenv("BLUESMIND_BASE_URL"),
)
glm = LLM(  # roadmap architect
    model="glm-4.6",
    api_key=os.getenv("BLUESMIND_API_KEY"),
    base_url=os.getenv("BLUESMIND_BASE_URL"),
)
claude = LLM(  # this will search the web
    model="claude-sonnet-4.5",
    api_key=os.getenv("NARAROUTER_API_KEY"),
    base_url=os.getenv("NARAROUTER_BASE_URL"),
)
claude_haiku = LLM(  # this will review the quality
    model="claude-haiku-4.5",
    api_key=os.getenv("NARAROUTER_API_KEY"),
    base_url=os.getenv("NARAROUTER_BASE_URL"),
)
mistral = LLM(  # query generator
    model="mistral-large",
    api_key=os.getenv("NARAROUTER_API_KEY"),
    base_url=os.getenv("NARAROUTER_BASE_URL"),
)

minimax = LLM(  # query generator
    model="minimax-m2.7",
    api_key=os.getenv("GENERALCOMPUTE_API_KEY"),
    base_url=os.getenv("GENERALCOMPUTE_BASE_URL"),
)


@CrewBase
class TheRoadmapper:
    """TheRoadmapper crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["analyst"],  # type: ignore[index]
            verbose=True,
            llm=minimax,
            tools=[SerperDevTool()],
        )

    @agent
    def query_generator(self) -> Agent:
        return Agent(
            config=self.agents_config["query_generator"],
            llm=minimax,
            verbose=True,
        )

    @agent
    def resource_hunter(self) -> Agent:
        return Agent(
            config=self.agents_config["resource_hunter"],  # type: ignore[index]
            verbose=True,
            llm=minimax,
            tools=[SerperDevTool()],
        )

    @agent
    def roadmap_architect(self) -> Agent:
        return Agent(
            config=self.agents_config["roadmap_architect"],  # type: ignore[index]
            llm=minimax,
            verbose=True,
        )

    @agent
    def quality_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config["quality_reviewer"],  # type: ignore[index]
            llm=minimax,
            verbose=True,
        )

    @agent
    def roadmap_editor(self) -> Agent:
        return Agent(
            config=self.agents_config["roadmap_editor"],  # type: ignore[index]
            llm=minimax,
            verbose=True,
            tools=[SerperDevTool()],
        )

    @task
    def analyze_topic_task(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_topic_task"],
            output_pydantic=AnalysisOutput,
        )

    @task
    def query_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config["query_generation_task"],
            output_pydantic=QueryOutput,
        )

    @task
    def find_resources_task(self) -> Task:
        return Task(
            config=self.tasks_config["find_resources_task"],
            output_pydantic=ResourceOutput,
        )

    @task
    def build_roadmap_task(self) -> Task:
        return Task(
            config=self.tasks_config["build_roadmap_task"],
            output_pydantic=Roadmap,
        )

    @task
    def review_roadmap_task(self) -> Task:
        return Task(
            config=self.tasks_config["review_roadmap_task"],
            output_pydantic=ReviewOutput,
        )

    @task
    def edit_roadmap_task(self) -> Task:
        return Task(
            config=self.tasks_config["edit_roadmap_task"],
            output_pydantic=Roadmap,
        )

    @task
    def review_revision_task(self) -> Task:
        return Task(
            config=self.tasks_config["review_revision_task"],
            output_pydantic=ReviewOutput,
        )

    @crew
    def research_crew(self) -> Crew:
        """Create the research crew"""
        return Crew(
            agents=[self.analyst(), self.query_generator(), self.resource_hunter()],
            tasks=[
                self.analyze_topic_task(),
                self.query_generation_task(),
                self.find_resources_task(),
            ],
            process=Process.sequential,
            verbose=True,
            tracing=True,
        )

    @crew
    def assembly_crew(self) -> Crew:
        """Creates the assembly crew"""
        return Crew(
            agents=[self.roadmap_architect(), self.quality_reviewer()],
            tasks=[self.build_roadmap_task(), self.review_roadmap_task()],
            process=Process.sequential,
            tracing=True,
            verbose=True,
        )

    @crew
    def editor_crew(self) -> Crew:
        """Create the roadmap editor crew"""
        return Crew(
            agents=[self.roadmap_editor()],
            tasks=[self.edit_roadmap_task()],
            process=Process.sequential,
            verbose=True,
            tracing=True,
        )

    @crew
    def review_crew(self) -> Crew:
        """Create the reviewer crew used after edits"""
        return Crew(
            agents=[self.quality_reviewer()],
            tasks=[self.review_revision_task()],
            process=Process.sequential,
            verbose=True,
            tracing=True,
        )
