
from .base_step import BaseStep
from abc import abstractmethod
from apps.adapters.markdown_adapter import MarkdownAdapter 

class MultipleStep(BaseStep):

    @abstractmethod 
    def _get_items_for_processing(self, inputs: dict[str, str]) -> list:
        """Returns a list of items (e.g., split plans, plot file contents) to process."""
        pass

    @abstractmethod 
    def _get_item_content(self, item, inputs: dict[str, str]) -> str:
        """Extracts/reads the content string from an item (which might be a string, a file path, etc.)."""
        pass

    @abstractmethod 
    def _format_prompt_for_item(self, inputs: dict[str, str], item_content: str, index: int, total: int) -> str:
        """Formats the prompt for a specific item."""
        pass

    def run(self): 
        """The refactored common logic for steps that produce multiple outputs."""
        if not self.is_enable:
            print(f"INFO: Step '{self.step.name}' is disabled or not initialized.")
            return

        inputs = self._read_inputs()
        if inputs is None: return

        items = self._get_items_for_processing(inputs)
        total_items = len(items)

        for idx, item in enumerate(items):
            item_content = self._get_item_content(item, inputs)

            full_prompt = self._format_prompt_for_item(inputs, item_content, idx, total_items)

            result = self.communicator.run(
                prompt=full_prompt
            )

            if result is None:
                print(f"WARNING: Communicator returned no result for step '{self.step.name}'.")
                continue

            output_path = self._get_output_path()
            output_path = self._rename_output_path(output_path , idx)
            MarkdownAdapter.write_file(output_path, result)
            print(f"INFO: {self.step.name.capitalize()}: Result has been written to", output_path)