#!/usr/bin/env python
import sys
import warnings
import json

from the_roadmapper.crew import TheRoadmapper
from the_roadmapper.flow import RoadmapFlow

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    flow= RoadmapFlow()
    flow.state.topic="video editing"
    flow.kickoff()