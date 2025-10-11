
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
        plan = self._read_file(self.input_plan_path, "plan")
        
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

    def _format_prompt_by_plan(self,inputs: dict[str, str] , plan: str , idx : int , full_idx : int) -> str:
         return (
            f"{self.prompt}\n"
            f"plan:{idx + 1}/{full_idx}\n"
            f"{plan}\n"
            f"# canon\n"
            f"{inputs['canon']}"
        )
    


    def run_plots(self):
        if not self.is_enable:
            print(f"INFO: Step '{self.step.name}' is disabled or not initialized.")
            return
        
        inputs = self._read_inputs()
        if inputs is None: return None
        self._split_content_into_plans(inputs['plan'])

        for idx, plan in enumerate(self._plans):
            prompt = self._format_prompt_by_plan(inputs, plan , idx , len(self._plans))
            result = self.communicator.run(
                prompt=prompt
            )

            if result is None:
                print(f"WARNING: Communicator returned no result for step '{self.step.name}'.")
                return
            
            output_path = self._get_output_path()
            output_path = self._rename_output_path(output_path , idx)
            self.write_file(output_path, result)
            print(f"INFO: {self.step.name.capitalize()}: Result has been written to", output_path)
