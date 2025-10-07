
import os

from apps.adapters.yaml_adapter import YamlAdapter
from apps.core.steps.base_step import BaseStep
from apps.domains.workflow_step import WorkflowStep

class Recorder(BaseStep):
    def __init__(self, input_memo_path: str, output_note_path: str):
        super().__init__(WorkflowStep.RECORDER)
        self.input_memo_path = input_memo_path
        self.output_note_path = output_note_path

    def _read_file(self, path: str, file_name: str) -> str | None:
        if not os.path.exists(path):
            print(f"info:{file_name} '{path}' does not exist.")
            return None
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def _read_inputs(self) -> dict[str, str] | None:
        memo = self._read_file(self.input_memo_path, "memo")
        return {"memo": memo} if memo is not None else None
        
    def _format_prompt(self, inputs: dict[str, str]) -> str:
        # Recorder のプロンプト形式に合わせて組み立て
        return f"{self.prompt}\n{inputs['memo']}"

    def _get_output_path(self) -> str:
        return self.output_note_path

