import os
import re
import json
import importlib
from langchain.llms import OpenAI

class LLM:

    def __init__(self, model="OpenAI", **model_params):
        # Set api_key from model_params or environment variable
        self.api_key = model_params.get('api_key') or os.environ.get('DREAM_MY_PLOTS_LLM_API_KEY')
        if 'api_key' in model_params:
            del model_params['api_key']  # Remove api_key from model_params to avoid duplication

        self.model_params = model_params

        os.environ[f"{model.upper()}_API_KEY"] = self.api_key or ""

        # Check if model is a string (model type name) or already an instance of a model
        if isinstance(model, str):
            # Dynamically import and initialize the model based on the string
            try:
                module = importlib.import_module("langchain.chat_models")
                ModelClass = getattr(module, f"Chat{model}")  # Get the class from the module
                self.model = ModelClass(model_name=model_params.pop('model_name', "gpt-4"), 
                                        temperature=model_params.pop('temperature', 0.7), 
                                        # max_tokens=model_params.pop('max_tokens', ''),
                                        model_kwargs=model_params)
            except AttributeError:
                raise ValueError(f"Model type '{model}' is not supported.")
        else:
            # Directly use the provided model object
            self.model = model

    def predict(self, prompt, **kwargs):
        # Combine model-specific parameters with any additional parameters provided at call time
        result = self.model.invoke(prompt)
        
        return result.content
