import os
from abc import ABC, abstractmethod

from adapters.ai_adapter import AiAdapter
from apps.adapters.yaml_adapter import YamlAdapter
from apps.utils.prompt_reader import PromptReader
from apps.domains.workflow_step import WorkflowStep

class BaseStep(ABC):
    def __init__(self ,step: WorkflowStep):
        self.step = step
        self.ai_adapter = AiAdapter()
        self.prompt : str | None = None

    @property
    def is_enable(self) -> bool:
        return self.ai_adapter.is_enable and self.prompt is not None
    
    def _get_api_key(self) -> str | None:
        api_key_path = self.get_config_value("api_key_path", None)
        if not api_key_path or not os.path.exists(api_key_path):
            return None
        with open(api_key_path, "r", encoding="utf-8") as f:
                return f.read().strip()
    
    def get_config_value(self, key: str, default=None):
        return YamlAdapter.get(key, default)

    def initialize(self):
        model_name = self.get_config_value("model_name")
        api_key = self._get_api_key()
        if model_name is None or api_key is None:
            print("INFO: Model name or API key is not configured properly.")
            return
        self.ai_adapter.initialize(model_name=model_name, api_key=api_key)

    def read_prompt(self):       
        self.prompt = PromptReader.read(self.step)
        if self.prompt is None:
            print(f"INFO: Prompt for step '{self.step.name}' could not be loaded.")
        else:
            print(f"INFO: Prompt for step '{self.step.name}' loaded successfully.")

    @abstractmethod
    def run(self):
        pass
    

    def write_file(self, file_path: str, content: str):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"INFO: File '{file_path}' was written.")