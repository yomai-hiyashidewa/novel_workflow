from enum import Enum, auto

class WorkflowStep(Enum):
    TESTER = "tester"
    RECORDER = "recorder"
    RESEARCHER = "researcher"
    PLANNER = "planner"
    PLOTTER = "plotter"
    WRITER = "writer"
    EDITOR = "editor"
    F_WRITER = "f_writer"
    ILLUSTRATOR = "illustrator"
    ALL = "all"