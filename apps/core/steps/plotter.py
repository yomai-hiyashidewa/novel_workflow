
import os
from typing import List

from apps.adapters.yaml_adapter import YamlAdapter
from apps.core.steps.base_step import BaseStep
from apps.domains.workflow_step import WorkflowStep

class Plotter(BaseStep):
    def __init__(self, input_plan_path: str, canon_path: str, output_plot_path: str):
        super().__init__(WorkflowStep.PLOTTER)
        self.input_plan_path = input_plan_path
        self.canon_path = canon_path
        self.output_plot_path = output_plot_path
        self._plans : List[str] = []

    def _read_inputs(self) -> dict[str, str] | None:
        plan = self._read_file(self.input_plan_path)
        
        canon = self._read_canon_directory(self.canon_path)

        return {"plan": plan, "canon": canon}

    def _format_prompt(self, inputs: dict[str, str]) -> str:
        pass

    def _get_output_path(self) -> str:
        return self.output_plot_path


    def _split_content_into_plans(self, content: str) -> None:
        lines = content.strip().split('\n')
        current_section: List[str] = []
        found_first_header = False

        for line in lines:
            stripped_line = line.strip()
            
            if stripped_line.startswith("### "):
                if found_first_header:
                    self._store_section(current_section)
                    current_section = []
                
                found_first_header = True
                current_section.append(line)
            elif found_first_header:
                current_section.append(line)


        if current_section:
            self._store_section(current_section)

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
            f"plan:{index + 1}/{total}\n"
            f"{item_content}\n"
            f"# canon\n"
            f"{inputs['canon']}"
        )
    