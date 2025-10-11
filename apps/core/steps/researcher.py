
import os
from apps.core.steps.base_step import BaseStep
from apps.domains.workflow_step import WorkflowStep

class Researcher(BaseStep):
    def __init__(self, input_note_path="note.md", input_research_path="research.md", output_setting_path="setting.md"):
        super().__init__(WorkflowStep.RESEARCHER)
        self.input_note_path = input_note_path
        self.input_research_path = input_research_path
        self.output_setting_path = output_setting_path

    def _read_inputs(self) -> dict[str, str] | None:
        note = self._read_file(self.input_note_path)
        if note is None: return None
        
        research = self._read_file(self.input_research_path)
        if research is None: return None
        
        return {"note": note, "research": research}
        
    def _format_prompt(self, inputs: dict[str, str]) -> str:
        return (
            f"{self.prompt}\n"
            f"# note.md\n"
            f"{inputs['note']}\n"
            f"# research.md\n"
            f"{inputs['research']}"
        )

    def _get_output_path(self) -> str:
        return self.output_setting_path
    
    def _get_items_for_processing(self, inputs: dict[str, str]) -> list:
        """Returns a list of items (e.g., split plans, plot file contents) to process."""
        pass

    def _get_item_content(self, item, inputs: dict[str, str]) -> str:
        """Extracts/reads the content string from an item (which might be a string, a file path, etc.)."""
        pass

    def _format_prompt_for_item(self, inputs: dict[str, str], item_content: str, index: int, total: int) -> str:
        """Formats the prompt for a specific item."""
        pass
