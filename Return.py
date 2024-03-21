# Return.py

"""
Class wraps the return value with the accoutrement's Java requires for a runtime exception class.
"""


class Return(Exception):
    def __init__(self, value):
        super().__init__()
        self.value = value # Return value
