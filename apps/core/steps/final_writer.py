
import os
from typing import List

from apps.adapters.yaml_adapter import YamlAdapter
from apps.core.steps.single_step import SingleStep
from apps.domains.workflow_step import WorkflowStep
from apps.adapters.markdown_adapter import MarkdownAdapter

class FinalWriter(SingleStep):
    def __init__(self, input_novel_path: str, canon_path: str, output_novel_path: str):
        super().__init__(WorkflowStep.F_WRITER)
        self.input_novel_path = input_novel_path
        self.canon_path = canon_path
        self.output_novel_path = output_novel_path

    def _read_inputs(self) -> dict[str, str] | None:
        novels : str = ""
        for file in self._list_markdown_files(self.input_novel_path):
            file_path = os.path.join(self.input_novel_path, file)
            content = MarkdownAdapter.read_file(file_path)
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
    
    def _get_output_path(self) -> str:
        return self.output_novel_path
    