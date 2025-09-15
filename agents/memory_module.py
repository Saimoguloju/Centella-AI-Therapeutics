# agents/memory_module.py
"""Memory Module for maintaining session history and context."""

import json
import os
from typing import Any, Dict, Optional
from datetime import datetime
from .base_agent import BaseAgent


class MemoryModule(BaseAgent):
    """Module responsible for storing and retrieving session memory."""
    
    def __init__(self, memory_file: str = "session_memory.json"):
        super().__init__(
            name="MemoryModule",
            description="Maintains session history and context across queries"
        )
        self.memory_file = memory_file
        self.memory = self._load_memory()
    
    def _load_memory(self) -> Dict[str, Any]:
        """Load memory from file if it exists."""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    self.log_execution(f"Loaded memory from {self.memory_file}")
                    return json.load(f)
            except Exception as e:
                self.log_execution(f"Error loading memory: {e}")
        
        # Initialize new memory
        return {
            "session_id": datetime.now().isoformat(),
            "last_target": None,
            "last_library_size": None,
            "query_history": [],
            "results_history": []
        }
    
    def save_memory(self):
        """Save current memory to file."""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.memory, f, indent=2)
            self.log_execution(f"Memory saved to {self.memory_file}")
        except Exception as e:
            self.log_execution(f"Error saving memory: {e}")
    
    def update_context(self, query_data: Dict[str, Any], results: Dict[str, Any]):
        """Update memory with latest query and results.
        
        Args:
            query_data: The input query data
            results: The results from the screening
        """
        # Update last values
        if 'target' in query_data:
            self.memory['last_target'] = query_data['target']
        if 'library_size' in query_data:
            self.memory['last_library_size'] = query_data['library_size']
        
        # Add to history
        self.memory['query_history'].append({
            "timestamp": datetime.now().isoformat(),
            "query": query_data
        })
        
        # Store summary of results
        if results:
            result_summary = {
                "timestamp": datetime.now().isoformat(),
                "target": results.get('target_id'),
                "best_score": results.get('best_score'),
                "num_hits": len(results.get('top_hits', []))
            }
            self.memory['results_history'].append(result_summary)
        
        # Keep only last 10 queries
        if len(self.memory['query_history']) > 10:
            self.memory['query_history'] = self.memory['query_history'][-10:]
            self.memory['results_history'] = self.memory['results_history'][-10:]
        
        self.save_memory()
    
    def get_last_target(self) -> Optional[str]:
        """Get the last used target."""
        return self.memory.get('last_target')
    
    def get_last_library_size(self) -> Optional[int]:
        """Get the last used library size."""
        return self.memory.get('last_library_size')
    
    def get_context(self) -> Dict[str, Any]:
        """Get current memory context."""
        return {
            "last_target": self.memory.get('last_target'),
            "last_library_size": self.memory.get('last_library_size'),
            "queries_count": len(self.memory.get('query_history', [])),
            "session_id": self.memory.get('session_id')
        }
    
    def clear_memory(self):
        """Clear all memory."""
        self.memory = {
            "session_id": datetime.now().isoformat(),
            "last_target": None,
            "last_library_size": None,
            "query_history": [],
            "results_history": []
        }
        self.save_memory()
        self.log_execution("Memory cleared")
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute memory operations.
        
        Args:
            input_data: Dictionary with operation type
            
        Returns:
            Dictionary with memory operation results
        """
        operation = input_data.get('operation', 'get_context')
        
        if operation == 'get_context':
            return {
                "context": self.get_context(),
                "status": "success"
            }
        elif operation == 'clear':
            self.clear_memory()
            return {
                "message": "Memory cleared",
                "status": "success"
            }
        else:
            return {
                "error": f"Unknown operation: {operation}",
                "status": "failed"
            }
