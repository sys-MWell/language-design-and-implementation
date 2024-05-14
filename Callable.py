# Callable.py
from abc import ABC, abstractmethod
from typing import List, Any

class Callable(ABC):
    """
    Represents any StalingScript object that can be called like a function.
    This includes user-defined functions and other entities that can be "called" within the language.
    """
    @abstractmethod
    def arity(self) -> int:
        """
        Returns the number of arguments the callable expects.
        """
        pass

    @abstractmethod
    def call(self, interpreter, arguments: List[Any]) -> Any:
        """
        Calls the callable with the provided arguments.
        """
        pass
