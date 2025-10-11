
import os
from typing import List

from apps.adapters.yaml_adapter import YamlAdapter
from apps.core.steps.multiple_step import MultipleStep
from apps.domains.workflow_step import WorkflowStep
from apps.adapters.markdown_adapter import MarkdownAdapter  

class Illustrator(MultipleStep):
    def __init__(self, input_novel_path: str, canon_path: str, output_illustration_path: str):
        super().__init__(WorkflowStep.ILLUSTRATOR)
        self.input_novel_path = input_novel_path
        self.canon_path = canon_path
        self.output_illustration_path = output_illustration_path

    def _read_inputs(self) -> dict[str, str] | None:
        
        canon = self._read_canon_directory(self.canon_path, with_thumbnail=True)

        return {"canon": canon}

    def _get_output_path(self) -> str:
        return self.output_illustration_path
    
    def _get_items_for_processing(self, inputs: dict[str, str]) -> list:
        plots = self._list_markdown_files(self.input_novel_path)
        return plots
    
    def _get_item_content(self, item: str, inputs: dict[str, str]) -> str:
        item_path = os.path.join(self.input_novel_path, item)
        item = MarkdownAdapter.read_file(item_path)
        return item

    def _format_prompt_for_item(self, inputs: dict[str, str], item_content: str, index: int, total: int) -> str:
        return (
            f"{self.prompt}\n"
            f"novel:{index + 1}/{total}\n"
            f"{item_content}\n"
            f"# canon\n"
            f"{inputs['canon']}"
        )