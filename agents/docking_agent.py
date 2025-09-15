# agents/docking_agent.py
"""Mock Docking Agent for simulating molecular docking."""

import hashlib
from typing import Any, Dict, List
from .base_agent import BaseAgent


class DockingAgent(BaseAgent):
    """Agent responsible for mock molecular docking simulations."""
    
    def __init__(self):
        super().__init__(
            name="DockingAgent",
            description="Performs mock molecular docking and assigns scores"
        )
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform mock docking simulation.
        
        Args:
            input_data: Dictionary containing 'molecules' and 'target_id'
            
        Returns:
            Dictionary with docking results
        """
        if not self.validate_input(input_data, ['molecules']):
            return {"error": "Missing molecules field"}
        
        molecules = input_data['molecules']
        target_id = input_data.get('target_id', 'UNKNOWN')
        
        self.log_execution(f"Starting mock docking for {len(molecules)} molecules against {target_id}")
        
        # Perform mock docking
        docking_results = self._perform_docking(molecules, target_id)
        
        self.log_execution(f"Docking completed for {len(docking_results)} molecules")
        
        return {
            "docking_results": docking_results,
            "target_id": target_id,
            "status": "success"
        }
    
    def _perform_docking(self, molecules: List[Dict[str, str]], target_id: str) -> List[Dict[str, Any]]:
        """Perform mock docking for each molecule.
        
        Uses deterministic scoring based on SMILES hash.
        Score = -(hash(smiles + target_id) % 7 + 4) for range -4 to -10
        
        Args:
            molecules: List of molecules with SMILES
            target_id: Target protein ID
            
        Returns:
            List of docking results
        """
        results = []
        
        for mol in molecules:
            ligand_id = mol['ligand_id']
            smiles = mol['smiles']
            
            # Generate deterministic score based on SMILES and target
            combined = f"{smiles}{target_id}"
            hash_value = int(hashlib.md5(combined.encode()).hexdigest(), 16)
            base_score = -(hash_value % 7 + 4)
            
            # Add some decimal precision for realism
            decimal_part = (hash_value % 100) / 100
            docking_score = base_score - decimal_part
            
            results.append({
                "ligand_id": ligand_id,
                "smiles": smiles,
                "docking_score": round(docking_score, 2)
            })
        
        return results
