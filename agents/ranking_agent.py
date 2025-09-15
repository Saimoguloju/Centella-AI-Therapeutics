# agents/ranking_agent.py
"""Scoring & Ranking Agent for selecting top molecules."""

from typing import Any, Dict, List
from .base_agent import BaseAgent


class RankingAgent(BaseAgent):
    """Agent responsible for ranking molecules and selecting top hits."""
    
    def __init__(self):
        super().__init__(
            name="RankingAgent",
            description="Ranks molecules by docking score and selects top hits"
        )
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Rank molecules and select top hits.
        
        Args:
            input_data: Dictionary containing 'docking_results'
            
        Returns:
            Dictionary with ranked results and top hits
        """
        if not self.validate_input(input_data, ['docking_results']):
            return {"error": "Missing docking_results field"}
        
        docking_results = input_data['docking_results']
        top_n = input_data.get('top_n', 5)  # Default to top 5
        
        self.log_execution(f"Ranking {len(docking_results)} molecules")
        
        # Sort by docking score (lower is better)
        ranked_results = sorted(docking_results, key=lambda x: x['docking_score'])
        
        # Add rank
        for i, result in enumerate(ranked_results, 1):
            result['rank'] = i
        
        # Select top hits
        top_hits = ranked_results[:top_n]
        
        self.log_execution(f"Selected top {len(top_hits)} hits")
        
        return {
            "ranked_results": ranked_results,
            "top_hits": top_hits,
            "best_score": top_hits[0]['docking_score'] if top_hits else None,
            "status": "success"
        }
