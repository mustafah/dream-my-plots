

class Prompt:

    def __init__(self, prompt="", df=None, template = None, previous_code="", previous_error=""):

        lines = prompt.split("\n")
        cleaned_lines = [line for line in lines if not line.strip().startswith("#")]
        cleaned_text = "\n".join(cleaned_lines)
        self.prompt = cleaned_text
        self.template = template
        self.df = df
        self.previous_code = previous_code
        self.previous_error = previous_error

    def input_data_str(self):
        if self.df is not None:
            return f"""
```python
# pandas DataFrame first 5 rows
'''
{self.df.head(5)}
'''
# DataFrame columns
'''
{self.df.columns.to_list()}
'''

# pandas data frame variable is df,
# don't declare or redfine the df variable in your code at all,
# don't put any data of df in your response
```
            """
        else:
            pass


    @property
    def value(self):

    # If a template is provided, use it with the appropriate parameters
        if self.template:
            # Assuming the template can accept and process these parameters
            return self.template.render(df=self.df,
                                        prompt=self.prompt,
                                        previous_code=self.previous_code,
                                        previous_error=self.previous_error)
        else:
            result = f"""Create a plot in Python with seaborn (more preferable), if you can't use matplotlib package (less preferable)

    Input data:

    {self.input_data_str()}


    Plot should contain: {self.prompt}

    Initial python code to be updated        

    ```python
    # TODO import required dependencies
    # TODO Try to avoid any deprecated function entirely if possible
    # TODO use cyberpunk theme by default for styling, by using ' mplcyberpunk ' pip package, and call to ` plt.style.use("cyberpunk") `
    # TODO don't add more colors or pallettes yourself more that cyberpunk theme, unless it is explicitly requested !
    # TODO Provide the plot
    # TODO show legends if it makes sense
    # TODO show plot title, axis titles
    ```

    Output Python code at the begining, and after that output minimal explaination please after the python code.
    """

            if self.previous_code != "":
                result += f"""
                
                You generated previously below code:
                {self.previous_code}

                It returned below error:
                {self.previous_error}

                Fix it. Do not return the same code again.
                """
            return result