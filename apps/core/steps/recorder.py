
import os

from apps.adapters.yaml_adapter import YamlAdapter
from apps.core.steps.base_step import BaseStep
from apps.domains.workflow_step import WorkflowStep

class Recorder(BaseStep):
    def __init__(self, input_memo_path: str, output_note_path: str):
        super().__init__(WorkflowStep.RECORDER)
        self.input_memo_path = input_memo_path
        self.output_note_path = output_note_path

    def _read_inputs(self) -> dict[str, str] | None:
        memo = self._read_file(self.input_memo_path)
        return {"memo": memo} if memo is not None else None
        
    def _format_prompt(self, inputs: dict[str, str]) -> str:
        return f"{self.prompt}\n{inputs['memo']}"

    def _get_output_path(self) -> str:
        return self.output_note_path
    
    def _get_items_for_processing(self, inputs: dict[str, str]) -> list:
        """Returns a list of items (e.g., split plans, plot file contents) to process."""
        pass

    def _get_item_content(self, item, inputs: dict[str, str]) -> str:
        """Extracts/reads the content string from an item (which might be a string, a file path, etc.)."""
        pass

    def _format_prompt_for_item(self, inputs: dict[str, str], item_content: str, index: int, total: int) -> str:
        """Formats the prompt for a specific item."""
        pass
    


