import os
from apps.domains.workflow_step import WorkflowStep

class PromptReader:
    PROMPT_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "prompts")

    @classmethod
    def read(cls, step: WorkflowStep) -> str | None:
        filename = step.value if step.value.endswith(".md") else f"{step.value}.md"
        prompt_path = os.path.join(cls.PROMPT_FOLDER, filename)

        prompt_path = os.path.abspath(prompt_path)
        if not os.path.exists(prompt_path):
            print(f"INFO: Prompt file '{prompt_path}' does not exist.")
            return None
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def get_prompt(step: WorkflowStep) -> str | None:
        return PromptReader.read(step)