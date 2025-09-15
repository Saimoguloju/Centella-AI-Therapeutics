# agents/base_agent.py
"""Base Agent class for all specialized agents in the virtual screening system."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)


class BaseAgent(ABC):
    """Abstract base class for all agents in the virtual screening system."""
    
    def __init__(self, name: str, description: str):
        """Initialize base agent.
        
        Args:
            name: Agent name
            description: Agent description
        """
        self.name = name
        self.description = description
        self.logger = logging.getLogger(self.name)
    
    @abstractmethod
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's main task.
        
        Args:
            input_data: Input data for the agent
            
        Returns:
            Dictionary containing the agent's output
        """
        pass
    
    def validate_input(self, input_data: Dict[str, Any], required_fields: list) -> bool:
        """Validate that required fields are present in input.
        
        Args:
            input_data: Input data to validate
            required_fields: List of required field names
            
        Returns:
            True if all required fields are present
        """
        for field in required_fields:
            if field not in input_data:
                self.logger.error(f"Missing required field: {field}")
                return False
        return True
    
    def log_execution(self, message: str):
        """Log agent execution details."""
        self.logger.info(f"[{self.name}] {message}")
