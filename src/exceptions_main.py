"""
Contains the exceptions used in the project.
"""


class NoResultFromFunctionError(Exception):
    """
    TODO
    """
    def __init__(self,  function: str = None, message: str = 'The function returned no value.'):
        self.message = message
        self.function = function

    def __str__(self):
        if self.function:
            return f'The function {self.function} did not provide a result.'
        return f'{self.message}'


class MissingArgumentError(Exception):
    """
    TODO
    """
    def __init__(self,  message: str = 'Missing argument.'):
        self.message = message
