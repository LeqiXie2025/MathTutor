import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BaseAgent(ABC):
    """Base class for all agents in the system."""

    def __init__(self, name: str = "BaseAgent"):
        self.name = name
        self.conversation_history: List[Dict[str, str]] = []

    @abstractmethod
    def process_input(self, input_text: str, **kwargs) -> str:
        """Process input and return response. Must be implemented by subclasses."""
        pass

    def add_to_history(self, role: str, content: str):
        """Add a message to conversation history."""
        self.conversation_history.append({"role": role, "content": content})

    def get_history(self) -> List[Dict[str, str]]:
        """Get the conversation history."""
        return self.conversation_history.copy()

    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history.clear()

    def __str__(self) -> str:
        return f"{self.name} (History: {len(self.conversation_history)} messages)"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"
