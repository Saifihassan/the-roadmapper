from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool
from pydantic import BaseModel,Field

from crewai import Agent, LLM
import os


# class SearchQuery(BaseModel):
#     """the search query"""
#     searchQuery:str 
#     Field(description="this is the search query that will be used to search the web")
# class searchQueryList(BaseModel):
#     """the list of search queries"""
#     searchList= list[SearchQuery]

gpt4o = LLM(                                    # analyze
    model="gpt-4o",
    api_key=os.getenv("BLUESMIND_API_KEY"),
    base_url=os.getenv("BLUESMIND_BASE_URL"),
)
glm = LLM(                                      # roadmap architect
    model="glm-4.6",
    api_key=os.getenv("BLUESMIND_API_KEY"),
    base_url=os.getenv("BLUESMIND_BASE_URL"),
)
claude = LLM(                                   # this will search the web
    model="claude-sonnet-4.5",
    api_key=os.getenv("NARAROUTER_API_KEY"),    
    base_url=os.getenv("NARAROUTER_BASE_URL"),
)
claude_haiku = LLM(                                   # this will review the quality 
    model="claude-haiku-4.5",
    api_key=os.getenv("NARAROUTER_API_KEY"),    
    base_url=os.getenv("NARAROUTER_BASE_URL"),
)
mistral = LLM(                                  #query generator
    model="mistral-large",
    api_key=os.getenv("NARAROUTER_API_KEY"),
    base_url=os.getenv("NARAROUTER_BASE_URL"),
)

minimax = LLM(                                  #query generator
    model="minimax-m2.7",
    api_key=os.getenv("GENERALCOMPUTE_API_KEY"),
    base_url=os.getenv("GENERALCOMPUTE_BASE_URL"),
)






@CrewBase
class TheRoadmapper():
    """TheRoadmapper crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['analyst'], # type: ignore[index]
            verbose=True,
            llm=minimax,
            tools=[SerperDevTool()]
        )
    @agent
    def query_generator(self)-> Agent:
        return Agent(
            config=self.agents_config['query_generator'],
            llm=minimax,
            verbose=True
            # output_pydantic=searchQueryList
        )
    @agent
    def resource_hunter(self) -> Agent:
        return Agent(
            config=self.agents_config['resource_hunter'], # type: ignore[index]
            verbose=True,
            llm=minimax,
            tools=[SerperDevTool()]
        )

    @agent
    def roadmap_architect(self) -> Agent:
        return Agent(
            config=self.agents_config['roadmap_architect'], # type: ignore[index]
            llm=minimax,
            verbose=True
        )

    @agent
    def quality_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['quality_reviewer'], # type: ignore[index]
            llm=minimax,
            verbose=True
            
        )
    
    @task
    def analyze_topic_task(self)->Task:
        return Task(
            config=self.tasks_config['analyze_topic_task']
        )
    @task
    def query_generation_task(self)->Task:
        return Task(
            config=self.tasks_config['query_generation_task']
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
    def research_crew(self) -> Crew:
        """Create the research crew"""
        return Crew(
            agents=[self.analyst(),self.query_generator(),self.resource_hunter()],
            tasks=[self.analyze_topic_task(),self.query_generation_task(),self.find_resources_task()],
            process=Process.sequential,
            verbose=True,
        )

    @crew
    def assembly_crew(self)->Crew:
        """Creates the assembly crew"""
        return Crew(
            agents=[self.roadmap_architect(),self.quality_reviewer()],
            tasks=[self.build_roadmap_task(),self.review_roadmap_task()],
            process=Process.sequential,
            verbose=True
        )