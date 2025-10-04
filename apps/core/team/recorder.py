
import os

from .base_team_mate import BaseTeamMate

class Recorder(BaseTeamMate):
    #PROMPT_PATH = "prompts/recorder.md"
    PROMPT_PATH = "C:\\Users\\user\\Documents\\projects\\novel_workflow\\prompts\\tester.md"
    
    def __init__(self, input_memo_path: str, input_img_path: str, output_note_path: str):
        super().__init__()
        self._memo_path = input_memo_path
        self._img_path = input_img_path
        self._note_path = output_note_path

        
    def initialize(self):
        super().initialize()
        self.read_prompt(self.PROMPT_PATH)
        
        
    def _read_memo(self) -> str | None:
        if not os.path.exists(self._memo_path):
            print(f"info:memo '{self._memo_path}' does not exist.")
            return None
        with open(self._memo_path, "r", encoding="utf-8") as f:
            return f.read()
        
    def run(self):
        memo = self._read_memo()
        if memo is None:
            return

        if self.is_enable is False:
            return

        result = self.ai_adapter.run(
            prompt=self.prompt
        )

        if result is None:
            return

        self.write_file(self._note_path, result)
