import os
from typing import List
from abc import ABC, abstractmethod

from communicators.gemini_communicator import GeminiCommunicator
from apps.adapters.yaml_adapter import YamlAdapter
from apps.utils.prompt_reader import PromptReader
from apps.domains.workflow_step import WorkflowStep
from apps.adapters.markdown_adapter import MarkdownAdapter

class BaseStep(ABC):
    def __init__(self ,step: WorkflowStep):
        self.step = step
        self.communicator = GeminiCommunicator()
        self.prompt : str | None = None

    @property
    def is_enable(self) -> bool:
        return self.communicator.is_enable and self.prompt is not None
    
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
        self.communicator.initialize(model_name=model_name, api_key=api_key)
        target_name = self.get_config_value("target_dir")
        target_dir = os.path.join(target_name, self.step.name.lower()) if target_name else None
        os.makedirs(target_dir, exist_ok=True)
        self._read_prompt()

   

    def _list_markdown_files(self , folder_path: str) -> List[str]:
        return MarkdownAdapter.list_markdown_files(folder_path)

    def _read_canon_directory(self, folder_path: str , with_thumbnail :bool = False) -> str | None:
        return MarkdownAdapter.read_canon_directory(folder_path, with_thumbnail)


    def _read_prompt(self):       
        self.prompt = PromptReader.read(self.step)
        if self.prompt is None:
            print(f"INFO: Prompt for step '{self.step.name}' could not be loaded.")
        else:
            print(f"INFO: Prompt for step '{self.step.name}' loaded successfully.")

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def _read_inputs(self) -> dict[str, str] | None:
        pass

    @abstractmethod
    def _get_output_path(self) -> str:
        pass

    def _rename_output_path(self, filename: str, index: int) -> str:
        base, ext = os.path.splitext(filename)
        return f"{base}_{index + 1}{ext}"

    @abstractmethod 
    def run(self):
        pass

    