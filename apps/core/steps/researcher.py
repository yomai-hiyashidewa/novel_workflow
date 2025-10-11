
import os
from apps.core.steps.single_step import SingleStep
from apps.domains.workflow_step import WorkflowStep
from apps.adapters.markdown_adapter import MarkdownAdapter

class Researcher(SingleStep):
    def __init__(self, input_note_path="note.md", input_research_path="research.md", output_setting_path="setting.md"):
        super().__init__(WorkflowStep.RESEARCHER)
        self.input_note_path = input_note_path
        self.input_research_path = input_research_path
        self.output_setting_path = output_setting_path

    def _read_inputs(self) -> dict[str, str] | None:
        note = MarkdownAdapter.read_file(self.input_note_path)
        if note is None: return None

        research = MarkdownAdapter.read_file(self.input_research_path)
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
    