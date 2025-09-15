# agents/summary_agent.py
"""Summary Writer Agent for generating screening reports."""

from typing import Any, Dict
from datetime import datetime
from .base_agent import BaseAgent


class SummaryAgent(BaseAgent):
    """Agent responsible for generating summary reports."""
    
    def __init__(self):
        super().__init__(
            name="SummaryAgent",
            description="Generates markdown summary reports of screening results"
        )
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary report.
        
        Args:
            input_data: Dictionary containing screening results
            
        Returns:
            Dictionary with markdown summary
        """
        # Check if summary should be skipped
        if input_data.get('skip_summary', False):
            self.log_execution("Summary generation skipped")
            return {"status": "skipped", "message": "Summary generation skipped"}
        
        if not self.validate_input(input_data, ['top_hits']):
            return {"error": "Missing required data for summary"}
        
        self.log_execution("Generating summary report")
        
        # Extract data
        target_id = input_data.get('target_id', 'Unknown')
        target_name = input_data.get('target_name', 'Unknown')
        library_size = input_data.get('library_size', 0)
        top_hits = input_data.get('top_hits', [])
        
        # Generate markdown summary
        summary = self._generate_markdown_summary(
            target_id, target_name, library_size, top_hits
        )
        
        self.log_execution("Summary report generated")
        
        return {
            "summary": summary,
            "status": "success"
        }
    
    def _generate_markdown_summary(self, target_id: str, target_name: str, 
                                   library_size: int, top_hits: list) -> str:
        """Generate markdown formatted summary.
        
        Args:
            target_id: PDB ID of target
            target_name: Name of target protein
            library_size: Number of molecules screened
            top_hits: List of top scoring molecules
            
        Returns:
            Markdown formatted summary string
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        summary = f"""# Virtual Screening Summary Report

## Screening Information
- **Date/Time**: {timestamp}
- **Target Protein**: {target_name} (PDB: {target_id})
- **Library Size**: {library_size} molecules
- **Screening Method**: Mock docking simulation
- **Scoring Function**: Deterministic hash-based scoring

## Top Hits

The following molecules showed the best binding affinity (lower scores = better binding):

| Rank | Ligand ID | SMILES | Docking Score |
|------|-----------|--------|---------------|
"""
        
        for hit in top_hits:
            summary += f"| {hit['rank']} | {hit['ligand_id']} | `{hit['smiles']}` | {hit['docking_score']} |\n"
        
        summary += f"""

## Statistical Summary
- **Best Docking Score**: {top_hits[0]['docking_score'] if top_hits else 'N/A'}
- **Worst Score in Top Hits**: {top_hits[-1]['docking_score'] if top_hits else 'N/A'}
- **Score Range**: {f"{abs(top_hits[-1]['docking_score'] - top_hits[0]['docking_score']):.2f}" if top_hits else 'N/A'}

## Recommendations
1. **Lead Compound**: {top_hits[0]['ligand_id'] if top_hits else 'None'} shows the most promising binding affinity
2. **Further Analysis**: Consider ADMET profiling for top 3 compounds
3. **Experimental Validation**: Proceed with in-vitro testing for compounds with scores < -7.0
4. **Structure Optimization**: Perform SAR analysis on the lead compound

## Next Steps
- [ ] ADMET profiling
- [ ] Molecular dynamics simulation
- [ ] In-vitro validation
- [ ] Lead optimization

---
*This is a mock simulation for demonstration purposes. Actual drug discovery requires sophisticated computational methods and experimental validation.*
"""
        
        return summary
