

from .base_step import BaseStep
from abc import abstractmethod
from apps.adapters.markdown_adapter import MarkdownAdapter 

class SingleStep(BaseStep):

    @abstractmethod
    def _format_prompt(self, inputs: dict[str, str]) -> str:
        pass
    
    def run(self):
        if not self.is_enable:
            print(f"INFO: Step '{self.step.name}' is disabled or not initialized.")
            return
        
        inputs = self._read_inputs()
        if inputs is None:
            return
        
        full_prompt = self._format_prompt(inputs)
        
        result = self.communicator.run(
            prompt=full_prompt
        )
        
        if result is None:
            print(f"WARNING: Communicator returned no result for step '{self.step.name}'.")
            return
        
        output_path = self._get_output_path()
        MarkdownAdapter.write_file(output_path, result)
        print(f"INFO: {self.step.name.capitalize()}: Result has been written to", output_path)
