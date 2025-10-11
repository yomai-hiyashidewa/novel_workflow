
import os
from typing import List

from apps.adapters.yaml_adapter import YamlAdapter
from apps.core.steps.base_step import BaseStep
from apps.domains.workflow_step import WorkflowStep

class FinalWriter(BaseStep):
    def __init__(self, input_novel_path: str, canon_path: str, output_novel_path: str):
        super().__init__(WorkflowStep.F_WRITER)
        self.input_novel_path = input_novel_path
        self.canon_path = canon_path
        self.output_novel_path = output_novel_path

    def _read_inputs(self) -> dict[str, str] | None:
        novels : str = ""
        for file in self._list_markdown_files(self.input_novel_path):
            file_path = os.path.join(self.input_novel_path, file)
            content = self._read_file(file_path)
            if content:
                novels += f"# {file}\n{content}\n"
        
        canon = self._read_canon_directory(self.canon_path)

        return {"canon": canon, "novels": novels}

    def _format_prompt(self, inputs: dict[str, str]) -> str:
        return (
            f"{self.prompt}\n"
            f"# canon\n"
            f"{inputs['canon']}\n"
            f"# novels\n"
            f"{inputs['novels']}"
        )
    
    def _get_items_for_processing(self, inputs: dict[str, str]) -> list:
        """Returns a list of items (e.g., split plans, plot file contents) to process."""
        pass

    def _get_item_content(self, item, inputs: dict[str, str]) -> str:
        """Extracts/reads the content string from an item (which might be a string, a file path, etc.)."""
        pass

    def _format_prompt_for_item(self, inputs: dict[str, str], item_content: str, index: int, total: int) -> str:
        """Formats the prompt for a specific item."""
        pass

    def _get_output_path(self) -> str:
        return self.output_novel_path
    