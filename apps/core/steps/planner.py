
import os

from apps.adapters.yaml_adapter import YamlAdapter
from apps.core.steps.base_step import BaseStep
from apps.domains.workflow_step import WorkflowStep

class Planner(BaseStep):
    def __init__(self, input_note_path: str, input_setting_path: str, canon_path: str, output_plan_path: str):
        super().__init__(WorkflowStep.PLANNER)
        self.input_note_path = input_note_path
        self.input_setting_path = input_setting_path
        self.canon_path = canon_path
        self.output_plan_path = output_plan_path

    def _read_inputs(self) -> dict[str, str] | None:
        note = self._read_file(self.input_note_path)
        setting = self._read_file(self.input_setting_path)
        canon = self._read_canon_directory(self.canon_path)

        return {"note": note, "setting": setting, "canon": canon}

    def _format_prompt(self, inputs: dict[str, str]) -> str:
         return (
            f"{self.prompt}\n"
            f"# note.md\n"
            f"{inputs['note']}\n"
            f"# setting.md\n"
            f"{inputs['setting']}\n"
            f"# canon\n"
            f"{inputs['canon']}"
        )

    def _get_output_path(self) -> str:
        return self.output_plan_path

