# agents/library_generator_agent.py
"""Library Generator Agent for creating mock molecule libraries."""

import random
from typing import Any, Dict, List
from .base_agent import BaseAgent


class LibraryGeneratorAgent(BaseAgent):
    """Agent responsible for generating libraries of mock molecules."""
    
    def __init__(self):
        super().__init__(
            name="LibraryGeneratorAgent",
            description="Generates mock molecule libraries with SMILES strings"
        )
        
        # Mock SMILES database
        self.smiles_database = [
            "CCO",  # Ethanol
            "c1ccccc1",  # Benzene
            "CC(=O)O",  # Acetic acid
            "CC(C)O",  # Isopropanol
            "c1ccc(O)cc1",  # Phenol
            "CC(=O)Nc1ccccc1",  # Acetanilide
            "CC(C)(C)O",  # tert-Butanol
            "c1ccc(cc1)C(=O)O",  # Benzoic acid
            "CCN(CC)CC",  # Triethylamine
            "C1CCCCC1",  # Cyclohexane
            "c1ccc(cc1)N",  # Aniline
            "CC(=O)OC",  # Methyl acetate
            "c1ccc(cc1)Cl",  # Chlorobenzene
            "CCOC(=O)C",  # Ethyl acetate
            "c1ccc(cc1)[N+](=O)[O-]",  # Nitrobenzene
            "CC(C)CC",  # Isopentane
            "c1ccc(cc1)C",  # Toluene
            "CC(=O)N",  # Acetamide
            "c1ccc(cc1)O[CH3]",  # Anisole
            "CCCCC",  # Pentane
            "C1CCC(CC1)O",  # Cyclohexanol
            "c1ccc2c(c1)cccc2",  # Naphthalene
            "CC(C)C(=O)O",  # Isobutyric acid
            "c1ccc(cc1)F",  # Fluorobenzene
            "CCCCCO",  # 1-Pentanol
            "c1ccc(cc1)Br",  # Bromobenzene
            "CC(C)C",  # Propane
            "c1ccc(cc1)I",  # Iodobenzene
            "CCOCC",  # Diethyl ether
            "c1ccc(cc1)CC",  # Ethylbenzene
        ]
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a library of mock molecules.
        
        Args:
            input_data: Dictionary containing 'library_size' field
            
        Returns:
            Dictionary with generated molecule library
        """
        # Check if custom SMILES file is provided
        if 'smiles_file' in input_data:
            self.log_execution("Using custom SMILES file")
            return {"status": "skipped", "message": "Using custom SMILES file"}
        
        if not self.validate_input(input_data, ['library_size']):
            library_size = 10  # Default size
        else:
            library_size = int(input_data['library_size'])
        
        self.log_execution(f"Generating library with {library_size} molecules")
        
        # Generate molecules
        molecules = self._generate_molecules(library_size)
        
        self.log_execution(f"Generated {len(molecules)} molecules")
        
        return {
            "molecules": molecules,
            "library_size": len(molecules),
            "status": "success"
        }
    
    def _generate_molecules(self, size: int) -> List[Dict[str, str]]:
        """Generate a list of mock molecules.
        
        Args:
            size: Number of molecules to generate
            
        Returns:
            List of dictionaries with ligand_id and SMILES
        """
        # Ensure we don't exceed database size
        actual_size = min(size, len(self.smiles_database))
        
        # Random sampling without replacement
        selected_smiles = random.sample(self.smiles_database, actual_size)
        
        molecules = []
        for i, smiles in enumerate(selected_smiles, 1):
            molecules.append({
                "ligand_id": f"L{i}",
                "smiles": smiles
            })
        
        return molecules
