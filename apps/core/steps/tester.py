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
    
    def _get_items_for_processing(self, inputs: dict[str, str]) -> list:
        """Returns a list of items (e.g., split plans, plot file contents) to process."""
        pass

    def _get_item_content(self, item, inputs: dict[str, str]) -> str:
        """Extracts/reads the content string from an item (which might be a string, a file path, etc.)."""
        pass

    def _format_prompt_for_item(self, inputs: dict[str, str], item_content: str, index: int, total: int) -> str:
        """Formats the prompt for a specific item."""
        pass


