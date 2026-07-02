#!/usr/bin/env python
import sys
import warnings
import json

from the_roadmapper.crew import TheRoadmapper

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    inputs = {
        'topic': 'agentic ai development',
        'revision_notes': ''
    }

    max_revisions = 2

    try:
        for attempt in range(max_revisions + 1):
            result = TheRoadmapper().crew().kickoff(inputs=inputs)

            if '"status": "approved"' in result.raw:
                print("✅ Roadmap approved!")
                print(result.raw)
                break

            if attempt < max_revisions:
                print(f"🔄 Needs revision (attempt {attempt + 1}/{max_revisions}). Retrying...")
                inputs['revision_notes'] = result.raw
            else:
                print("⚠️ Max revisions reached. Using last output.")
                print(result.raw)

    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")