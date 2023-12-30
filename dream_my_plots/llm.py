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
        # self.model_params[f"{model.upper()}_API_KEY"] = self.api_key

        # Set default model_name to GPT-4 for OpenAI if not provided
        # if 'model_name' not in self.model_params and model == "OpenAI":
        #     self.model_params['model_name'] = "gpt-4"  # Defaulting to "gpt-4"

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

# def main():
#     # Set your API key in environment as LLM_API_KEY or pass it directly
#     # os.environ['DREAMPLOT_LLM_API_KEY'] = "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"

#     # Example using a string to specify the model, no api_key provided so defaults to environment variable
#     llm = LLM(
#         "OpenAI",  # model: Indicates the type of model to use, in this case, "OpenAI".
#         # api_key = "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",
#         # model_name="gpt-4",  # model_name: The specific model of OpenAI to use, here "gpt-3.5-turbo".
#         temperature=0.7,  # temperature: Controls the randomness of the output. Higher values lead to more random completions.
#         max_tokens=100000,  # max_tokens: The maximum length of the generated text (in tokens).
#         top_p=1,  # top_p: Controls diversity via nucleus sampling: 1.0 means no nucleus sampling and 0<x<1 means sampling from the smallest set of words whose cumulative probability exceeds x.
#         frequency_penalty=0,  # frequency_penalty: Decreases the likelihood of repetition in generated text.
#         presence_penalty=0.6  # presence_penalty: Alters the likelihood of new language versus sticking with what's already mentioned.
#     )

#     prompt = "Translate the following English text to French: 'Hello, world!'"
#     response_openai = llm.predict(prompt)
#     print(response_openai)

# # if __name__ == "__main__":
# #     main()
