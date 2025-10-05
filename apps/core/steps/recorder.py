import os

from apps.core.steps.base_step import BaseStep
from apps.domains.workflow_step import WorkflowStep

class Recorder(BaseStep):
    def __init__(self, input_memo_path: str, output_note_path: str):
        super().__init__(WorkflowStep.RECORDER)
        self.input_memo_path = input_memo_path
        self.output_note_path = output_note_path

    def _read_memo(self) -> str | None:
        if not os.path.exists(self.input_memo_path):
            print(f"info:memo '{self.input_memo_path}' does not exist.")
            return None
        with open(self.input_memo_path, "r", encoding="utf-8") as f:
            return f.read()

    def initialize(self):
        super().initialize()
        self.read_prompt()

    def run(self):
        if not self.is_enable:
            return
        
        memo = self._read_memo()
        if memo is None:
            return
        
        prompt_with_memo = f"{self.prompt}\n{memo}"

        result = self.communicator.run(
            prompt=prompt_with_memo
        )
        if result is None:
            return
        self.write_file(self.output_note_path, result)
        print("Recorder: Note has been written to", self.output_note_path)