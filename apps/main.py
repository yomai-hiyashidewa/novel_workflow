import sys
import os
import argparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apps.core.directer import Director
from apps.domains.workflow_step import WorkflowStep

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a workflow step.")
    parser.add_argument(
        "--step",
        type=str,
        choices=[step.value for step in WorkflowStep],
        default=WorkflowStep.RECORDER.value,
        help="The workflow step to run."
    )
    args = parser.parse_args()

    director = Director()
    director.run(step=WorkflowStep(args.step))