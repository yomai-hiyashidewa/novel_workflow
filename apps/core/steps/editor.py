
import os
from typing import List

from apps.adapters.yaml_adapter import YamlAdapter
from apps.core.steps.base_step import BaseStep
from apps.domains.workflow_step import WorkflowStep

class Editor(BaseStep):
    def __init__(self, input_novel_path: str, canon_path: str, output_novel_path: str):
        super().__init__(WorkflowStep.EDITOR)
        self.input_novel_path = input_novel_path
        self.canon_path = canon_path
        self.output_novel_path = output_novel_path

    def _read_inputs(self) -> dict[str, str] | None:
        
        canon = self._read_canon_directory(self.canon_path)

        return {"canon": canon}

    def _format_prompt(self, inputs: dict[str, str]) -> str:
        pass

    def _get_output_path(self) -> str:
        return self.output_novel_path
    
    def _get_items_for_processing(self, inputs: dict[str, str]) -> list:
        plots = self._list_markdown_files(self.input_novel_path)
        return plots
    
    def _get_item_content(self, item: str, inputs: dict[str, str]) -> str:
        item_path = os.path.join(self.input_novel_path, item)
        item = self._read_file(item_path)
        return item

    def _format_prompt_for_item(self, inputs: dict[str, str], item_content: str, index: int, total: int) -> str:
        return (
            f"{self.prompt}\n"
            f"novel:{index + 1}/{total}\n"
            f"{item_content}\n"
            f"# canon\n"
            f"{inputs['canon']}"
        )