
import os
import shutil
from typing import Dict
from apps.adapters.yaml_adapter import YamlAdapter
from apps.domains.workflow_step import WorkflowStep
from apps.core.steps.recorder import Recorder
from apps.core.steps.researcher import Researcher
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
        researcher = Researcher()
        researcher.initialize()
        researcher.run()

    def _run_tester(self):
        tester = Tester()
        tester.initialize()
        tester.run()

    def run(self, step: WorkflowStep):
        if step == WorkflowStep.RECORDER:
            self._run_recorder()
        elif step == WorkflowStep.RESEARCHER:
            self._run_researcher()
        elif step == WorkflowStep.TESTER:
            self._run_tester()

    
     

        