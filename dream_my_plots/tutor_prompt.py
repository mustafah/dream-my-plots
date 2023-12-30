

class Prompt:

    def __init__(self, prompt="", df=None, x=None, y=None, z=None, previous_code="", previous_error="", data={}):

        lines = prompt.split("\n")
        cleaned_lines = [line for line in lines if not line.strip().startswith("#")]
        cleaned_text = "\n".join(cleaned_lines)
        self.prompt = cleaned_text
        self.df = df
        self.x, self.y, self.z = x, y, z
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

# pandas data frame variable is df, don't declare or redfine the df variable in your code at all
```
            """
        else:
            pass


    @property
    def value(self):
        v = f"""Create a plot in Python with seaborn or matplotlib package

Input data:

{self.input_data_str()}


Plot should contain: {self.prompt}

Initial python code to be updated        

```python
# TODO import required dependencies
# TODO Provide the plot
# TODO show if possible titles, and axis labels
```

Output Python code at the begining, and after that output minimal explaination please after the python code.
"""

        if self.previous_code != "":
            v += f"""
            
            You generated previously below code:
            {self.previous_code}

            It returned below error:
            {self.previous_error}

            Fix it. Do not return the same code again.
            """
        return v