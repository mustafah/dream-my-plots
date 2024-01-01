import pandas as pd
from .llm import LLM

from .prompt import Prompt

from .executor import Executor
from .logger import Logger

import os

class DreamMyPlots:

    def __init__(self, df, prompt = None, llm = None, api_key = None, dark = None, template = None):

        self.df = df
        if not hasattr(df, 'previous_error'):
            setattr(df, 'previous_error', None)
        if not hasattr(df, 'previous_code'):
            setattr(df, 'previous_code', None)
        self.prompt = prompt
        self.llm = llm
        self.template = template
        self.api_key = api_key
        self.dark = dark

        if prompt:
            self.dream(prompt)

    def dream(self, prompt):

        df = self.df
        p = Prompt(prompt, df, self.template, df.previous_code, df.previous_error)    

        Logger().log({"title": "💭 OpenAI prompt ...", "details": p.value})
        if self.llm:
            llm = self.llm
        else:
            llm = LLM(
                "OpenAI",  # model: Indicates the type of model to use, in this case, "OpenAI".
                api_key = self.api_key,
                model_name="gpt-4",  # model_name: The specific model of OpenAI to use, here "gpt-3.5-turbo".
                temperature=0.7,  # temperature: Controls the randomness of the output. Higher values lead to more random completions.
                # max_tokens=100,  # max_tokens: The maximum length of the generated text (in tokens).
                top_p=1,  # top_p: Controls diversity via nucleus sampling: 1.0 means no nucleus sampling and 0<x<1 means sampling from the smallest set of words whose cumulative probability exceeds x.
                frequency_penalty=0,  # frequency_penalty: Decreases the likelihood of repetition in generated text.
                presence_penalty=0.6  # presence_penalty: Alters the likelihood of new language versus sticking with what's already mentioned.
            )
        response = llm.predict(p.value)

        Logger().log({"title": "🔮 Suggested Response !", "details": response})

        if self.dark is not None:
            os.environ["DREAM_MY_PLOTS_THEME"] = 'dark' if self.dark else 'light'

        executor = Executor()
        error = executor.run(response, self.df,  globals(), locals())

        if error is not None:
            df.previous_error = error
            Logger().log({"title": "Error in code execution, Run again to fix ✅", "details": error})
