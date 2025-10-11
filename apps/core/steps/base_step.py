import os
from abc import ABC, abstractmethod

from communicators.gemini_communicator import GeminiCommunicator
from apps.adapters.yaml_adapter import YamlAdapter
from apps.utils.prompt_reader import PromptReader
from apps.domains.workflow_step import WorkflowStep

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

    def _read_file(self, path: str, file_name: str) -> str | None:
        if not os.path.exists(path):
            print(f"info:{file_name} '{path}' does not exist.")
            return None
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
        

    def _read_canon_directory(self, folder_path: str) -> str | None:

        if not os.path.isdir(folder_path):
            print(f"info: Directory '{folder_path}' does not exist or is not a directory.")
            return None

        all_content = []

        for root, _, files in os.walk(folder_path):
            for file_name in files:
                if file_name.endswith(".md"):
                    file_path = os.path.join(root, file_name)

              
                with open(file_path, "r", encoding="utf-8") as f:
                    all_content.append(f"### {file_name}\n")
                    all_content.append(f.read())
                    all_content.append("\n\n")

        if not all_content:
            return None
        return "".join(all_content).rstrip() 


    def _read_prompt(self):       
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


    @abstractmethod
    def _read_inputs(self) -> dict[str, str] | None:
        pass
    
    @abstractmethod
    def _format_prompt(self, inputs: dict[str, str]) -> str:
        pass

    @abstractmethod
    def _get_output_path(self) -> str:
        pass

    def _rename_output_path(self, filename: str, index: int) -> str:
        base, ext = os.path.splitext(filename)
        return f"{base}_{index + 1}{ext}"

    def run(self):
        if not self.is_enable:
            print(f"INFO: Step '{self.step.name}' is disabled or not initialized.")
            return
        
        # 1. 入力の読み込み
        inputs = self._read_inputs()
        if inputs is None:
            # 入力ファイルが見つからないなどの情報は _read_inputs 内で出力済み
            return
        
        # 2. プロンプトの組み立て
        full_prompt = self._format_prompt(inputs)
        
        # 3. コミュニケーターの実行
        result = self.communicator.run(
            prompt=full_prompt
        )
        
        if result is None:
            print(f"WARNING: Communicator returned no result for step '{self.step.name}'.")
            return
        
        # 4. 結果の書き込み
        output_path = self._get_output_path()
        self.write_file(output_path, result)
        print(f"INFO: {self.step.name.capitalize()}: Result has been written to", output_path)

