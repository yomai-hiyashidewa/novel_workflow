from apps.core.steps.base_step import BaseStep
from apps.domains.workflow_step import WorkflowStep

class Tester(BaseStep):
    def __init__(self):
        super().__init__(WorkflowStep.TESTER)

    def _read_inputs(self) -> dict[str, str] | None:
        return {"test": "test"}
        
    def _format_prompt(self, inputs: dict[str, str]) -> str:
        return f"{self.prompt}\n{inputs['test']}"

    def _get_output_path(self) -> str:
        return "test.md"    


