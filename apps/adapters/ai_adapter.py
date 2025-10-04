# ai_adapter.py
import os
import google.generativeai as genai
from google.generativeai import types
from typing import Optional

# 使用するモデル


class AiAdapter:
    
    _model: Optional[genai.GenerativeModel] = None

    def __init__(self):
        pass

    @property
    def is_enable(self) -> bool:
        return self._model is not None


    def initialize(self , model_name : str,api_key: str):
        if self._model is not None:
            return

        genai.configure(api_key=api_key)

        self._model = genai.GenerativeModel(model_name)
        print("AiAdapter: Successfully initialized the Gemini model.")
    

    def run(self, prompt : str) -> str | None:
        response = self._model.generate_content(
            prompt
        )
        print("AiAdapter: Editing completed")
        return response.text

    

   