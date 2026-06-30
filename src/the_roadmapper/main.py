#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from the_roadmapper.crew import TheRoadmapper

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'Agentic AI development'
    }

    try:
        TheRoadmapper().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
