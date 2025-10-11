
import os

from apps.adapters.yaml_adapter import YamlAdapter
from .single_step import SingleStep
from apps.domains.workflow_step import WorkflowStep
from apps.adapters.markdown_adapter import MarkdownAdapter

class Recorder(SingleStep):
    def __init__(self, input_memo_path: str, output_note_path: str):
        super().__init__(WorkflowStep.RECORDER)
        self.input_memo_path = input_memo_path
        self.output_note_path = output_note_path

    def _read_inputs(self) -> dict[str, str] | None:
        memo = MarkdownAdapter.read_file(self.input_memo_path)
        return {"memo": memo} if memo is not None else None
        
    def _format_prompt(self, inputs: dict[str, str]) -> str:
        return f"{self.prompt}\n{inputs['memo']}"

    def _get_output_path(self) -> str:
        return self.output_note_path
    


