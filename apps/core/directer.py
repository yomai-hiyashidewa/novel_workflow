
import os
import shutil
from typing import Dict
from apps.adapters.yaml_adapter import YamlAdapter
from apps.domains.workflow_step import WorkflowStep
from apps.core.steps.recorder import Recorder
from apps.core.steps.researcher import Researcher
from apps.core.steps.planner import Planner
from apps.core.steps.plotter import Plotter
from apps.core.steps.tester import Tester

class Director:
    def __init__(self):
        self._target_name = YamlAdapter.get("target_dir", ".")
        
        
    def _run_recorder(self):
        recorder_data = YamlAdapter.get_step(WorkflowStep.RECORDER.value, {})
        input_memo = recorder_data.get("input")
        output_note = recorder_data.get("output")
        input_memo_path = os.path.join(self._target_name, input_memo)
        output_note_path = os.path.join(self._target_name, WorkflowStep.RECORDER.value, output_note)
        recorder = Recorder(input_memo_path=input_memo_path, output_note_path=output_note_path)
        recorder.initialize()
        recorder.run()

    def _run_researcher(self):
        researcher_data = YamlAdapter.get_step(WorkflowStep.RESEARCHER.value, {})
        input_note = researcher_data.get("input_note")
        input_research = researcher_data.get("input_research")
        output = researcher_data.get("output")
        input_note_path = os.path.join(self._target_name, WorkflowStep.RECORDER.value, input_note)
        input_research_path = os.path.join(self._target_name, input_research)
        output_path = os.path.join(self._target_name, WorkflowStep.RESEARCHER.value, output)
        researcher = Researcher(input_note_path=input_note_path, input_research_path=input_research_path, output_setting_path=output_path)
        researcher.initialize()
        researcher.run()

    def _run_planner(self):
        canon_path = YamlAdapter.get("canon_path", None)
        planner_data = YamlAdapter.get_step(WorkflowStep.PLANNER.value, {})
        input_note = planner_data.get("input_note")
        input_setting = planner_data.get("input_setting")
        output = planner_data.get("output")
        input_note_path = os.path.join(self._target_name, WorkflowStep.RECORDER.value, input_note)
        input_setting_path = os.path.join(self._target_name, WorkflowStep.RESEARCHER.value, input_setting)
        output_path = os.path.join(self._target_name, WorkflowStep.PLANNER.value, output)
        planner = Planner(input_note_path=input_note_path, input_setting_path=input_setting_path, canon_path=canon_path, output_plan_path=output_path)
        planner.initialize()
        planner.run()

    def _run_plotter(self):
        canon_path = YamlAdapter.get("canon_path", None)
        plotter_data = YamlAdapter.get_step(WorkflowStep.PLOTTER.value, {})
        input_plan = plotter_data.get("input")
        output_plot = plotter_data.get("output")
        input_plan_path = os.path.join(self._target_name, WorkflowStep.PLANNER.value, input_plan)
        output_plot_path = os.path.join(self._target_name, WorkflowStep.PLOTTER.value, output_plot)
        plotter = Plotter(input_plan_path=input_plan_path, canon_path=canon_path, output_plot_path=output_plot_path)
        plotter.initialize()
        plotter.run_plots()

    def _run_tester(self):
        tester = Tester()
        tester.initialize()
        tester.run()

    def run(self, step: WorkflowStep):
        try:
            if step == WorkflowStep.RECORDER:
                self._run_recorder()
            elif step == WorkflowStep.RESEARCHER:
                self._run_researcher()
            elif step == WorkflowStep.TESTER:
                self._run_tester()
            elif step == WorkflowStep.PLANNER:
                self._run_planner()
            elif step == WorkflowStep.PLOTTER:
                self._run_plotter()
            elif step == WorkflowStep.WRITER:
                print("Writer step is not implemented yet.")
            elif step == WorkflowStep.ILLUSTRATOR:
                print("Illustrator step is not implemented yet.")
            else:
                print("All steps will be executed in order.")
        except Exception as e:
            print(f"Error occurred while running {step.value}: {e}")

    
     

        