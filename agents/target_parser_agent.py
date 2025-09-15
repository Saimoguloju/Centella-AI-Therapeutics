# agents/target_parser_agent.py
"""Target Parser Agent for validating and standardizing protein inputs."""

from typing import Any, Dict
from .base_agent import BaseAgent


class TargetParserAgent(BaseAgent):
    """Agent responsible for parsing and validating protein targets."""
    
    def __init__(self):
        super().__init__(
            name="TargetParserAgent",
            description="Validates and standardizes protein target inputs (PDB IDs or protein names)"
        )
        
        # Mock mapping of protein names to PDB IDs
        self.protein_mapping = {
            "EGFR": "1A4G",
            "ACE2": "6M0J",
            "BRAF": "5VAM",
            "ALK": "3LCS",
            "CDK2": "1HCK",
            "VEGFR": "3V2A",
            "BCL2": "2W3L",
            "HSP90": "3T0Z",
            "MTOR": "4JT5",
            "PI3K": "5XGH"
        }
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse and validate protein target.
        
        Args:
            input_data: Dictionary containing 'target' field
            
        Returns:
            Dictionary with standardized target information
        """
        if not self.validate_input(input_data, ['target']):
            return {"error": "Missing target field"}
        
        target = input_data['target'].strip().upper()
        self.log_execution(f"Parsing target: {target}")
        
        # Check if it's a PDB ID (4 characters)
        if len(target) == 4 and target.isalnum():
            self.log_execution(f"Validated PDB ID: {target}")
            return {
                "target_id": target,
                "chain": "A",
                "target_name": self._reverse_lookup(target),
                "status": "success"
            }
        
        # Check if it's a protein name
        elif target in self.protein_mapping:
            pdb_id = self.protein_mapping[target]
            self.log_execution(f"Mapped {target} to PDB ID: {pdb_id}")
            return {
                "target_id": pdb_id,
                "chain": "A",
                "target_name": target,
                "status": "success"
            }
        
        else:
            self.log_execution(f"Unknown target: {target}")
            return {
                "error": f"Unknown target: {target}",
                "status": "failed",
                "available_targets": list(self.protein_mapping.keys())
            }
    
    def _reverse_lookup(self, pdb_id: str) -> str:
        """Find protein name from PDB ID."""
        for name, id in self.protein_mapping.items():
            if id == pdb_id:
                return name
        return "Unknown"
