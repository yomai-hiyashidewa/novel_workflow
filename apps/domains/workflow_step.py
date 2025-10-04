from enum import Enum, auto

class WorkflowStep(Enum):
    TESTER = "tester"
    RECORDER = "recorder"
    RESEARCHER = "researcher"
    PLANNER = "planner"
    PLOTTER = "plotter"
    WRITER = "writer"
    ILLUSTRATOR = "illustrator"