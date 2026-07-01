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
        'topic': 'Cold sales outreach',
        'search_budget':6
    }

    try:
        TheRoadmapper().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
