from abc import ABC, abstractmethod
from typing import List, Any


class Callable(ABC):
    """
    Represents any Lox object that can be called like a function.

    This includes user-defined functions, class objects (for constructing
    new instances), and other entities that can be "called" within the Lox language.

    Subclasses must implement the call method, defining how the object is called,
    and the arity method, indicating the number of arguments the callable expects.
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
