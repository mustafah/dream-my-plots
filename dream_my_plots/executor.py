import os
import textwrap
from pygments import highlight
from pygments.lexers import PythonLexer
from IPython.display import display, HTML
from pygments.formatters import HtmlFormatter

class Executor:

    def run(self, code, df, globals_env=None, locals_env=None):
        wrap_width = 80
        try:
            python_code = ""
            before_text = []
            after_text = []
            code_started = False
            code_finished = False
            for line in code.split("\n"):

                if not line.strip().startswith("```"):
                    if code_started:
                        python_code += line + "\n"
                    elif not code_finished:
                        before_text.append(textwrap.fill(line, width=wrap_width))
                    else:
                        after_text.append(textwrap.fill(line, width=wrap_width))
                else:
                    if code_started:
                        code_started = False
                        code_finished = True
                    else:
                        code_started = True
                        code_finished = False
            
            
            print('\n'.join(item for item in before_text if item))

            if os.environ.get("DREAM_MY_PLOTS_THEME", "").lower() == 'dark':
                theme = "monokai"
            else:
                theme = "staroffice"
            formatter = HtmlFormatter(style=theme)
            formatted_python_code = highlight(python_code, PythonLexer(), formatter)
            style = formatter.get_style_defs('.highlight')
            style += '.highlight { background: transparent; }'
            html = f"<style>{style}</style>{formatted_python_code}"
            display(HTML(html))

            df.previous_code = python_code
            exec(python_code, globals_env, locals_env)

            print('\n'.join(item for item in after_text if item))

        except Exception as e:
            return str(e)
        return None