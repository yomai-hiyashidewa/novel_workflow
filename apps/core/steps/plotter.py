
import os
from typing import List

from apps.adapters.yaml_adapter import YamlAdapter
from apps.core.steps.multiple_step import MultipleStep
from apps.domains.workflow_step import WorkflowStep
from apps.adapters.markdown_adapter import MarkdownAdapter  

class Plotter(MultipleStep):
    def __init__(self, input_plan_path: str, canon_path: str, output_plot_path: str):
        super().__init__(WorkflowStep.PLOTTER)
        self.input_plan_path = input_plan_path
        self.canon_path = canon_path
        self.output_plot_path = output_plot_path
        self._synopsis : str = ""
        self._plans : List[str] = []

    def _read_inputs(self) -> dict[str, str] | None:
        plan = MarkdownAdapter.read_file(self.input_plan_path)

        canon = self._read_canon_directory(self.canon_path)

        return {"plan": plan, "canon": canon}

    def _get_output_path(self) -> str:
        return self.output_plot_path
    
    def _open_synopsis_block(self, stripped_line: str) -> None:
        self._synopsis_lines.append(stripped_line[3:].strip())
        self._in_synopsis_block = True

    def _close_synopsis_block(self) -> None:
        if self._in_synopsis_block:
            self._in_synopsis_block = False
            self._synopsis = "\n".join(self._synopsis_lines).strip()
            self._synopsis_lines = []

    def _handle_level_3_header(self, line: str) -> None:

        if self._found_first_header:
            self._store_section(self._current_section)
            self._current_section = []

        self._found_first_header = True
        self._current_section.append(line)


    def _split_content_into_plans(self, content: str) -> None:
        lines = content.strip().split('\n')

        self._current_section = []
        self._synopsis_lines = []
        self._in_synopsis_block = False
        self._found_first_header = False

        for line in lines:
            stripped_line = line.strip()

            if stripped_line.startswith("## "):
                self._open_synopsis_block(stripped_line)
            elif stripped_line.startswith("### "):
                self._close_synopsis_block()
                self._handle_level_3_header(line)
            elif self._found_first_header:
                self._current_section.append(line)
            elif self._in_synopsis_block:
                self._synopsis_lines.append(line)

        if self._current_section:
            self._store_section(self._current_section)

    def _store_section(self, section_lines: List[str]) -> None:
        while section_lines and not section_lines[-1].strip():
            section_lines.pop()
        
        self._plans.append("\n".join(section_lines))

    def _get_items_for_processing(self, inputs: dict[str, str]) -> list:
        self._split_content_into_plans(inputs['plan'])
        return self._plans

    def _get_item_content(self, item: str, inputs: dict[str, str]) -> str:
        return item

    def _format_prompt_for_item(self, inputs: dict[str, str], item_content: str, index: int, total: int) -> str:
         return (
            f"{self.prompt}\n"
            f"# synopsis\n"
            f"{self._synopsis}\n"
            f"plan:{index + 1}/{total}\n"
            f"{item_content}\n"
            f"# canon\n"
            f"{inputs['canon']}"
        )
    