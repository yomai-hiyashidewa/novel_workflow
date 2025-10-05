from apps.core.steps.base_step import BaseStep
from apps.domains.workflow_step import WorkflowStep

class Tester(BaseStep):
    def __init__(self):
        super().__init__(WorkflowStep.TESTER)

    def initialize(self):
        super().initialize()
        self.read_prompt()

    def run(self):
        if self.is_enable is False:
            return
        
        result = self.communicator.run(
            prompt=self.prompt
        )   
        if result is None:
            return
        print("Tester: Gemini Communicator returned result:")
        print(result)   