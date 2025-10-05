import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apps.core.directer import Director
from apps.domains.workflow_step import WorkflowStep

if __name__ == "__main__":
    director = Director()
    director.run(step=WorkflowStep.RECORDER)