from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool
@CrewBase
class TheRoadmapper():
    """TheRoadmapper crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['analyst'], # type: ignore[index]
            verbose=True
        )

    @agent
    def resource_hunter(self) -> Agent:
        return Agent(
            config=self.agents_config['resource_hunter'], # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool()]
        )

    @agent
    def roadmap_architect(self) -> Agent:
        return Agent(
            config=self.agents_config['roadmap_architect'], # type: ignore[index]
        )

    @agent
    def quality_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['quality_reviewer'], # type: ignore[index]
        )
    
    @task
    def analyze_topic_task(self)->Task:
        return Task(
            config=self.tasks_config['analyze_topic_task']
        )
    
    @task
    def find_resources_task(self)->Task:
        return Task(
            config= self.tasks_config['find_resources_task']
        )
    
    @task
    def build_roadmap_task(self)->Task:
        return Task(
            config=self.tasks_config['build_roadmap_task']
        )

    @task
    def review_roadmap_task(self)->Task:
        return Task(
            config=self.tasks_config['review_roadmap_task']
        )
    @crew
    def crew(self) -> Crew:
        """Creates the TheRoadmapper crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
