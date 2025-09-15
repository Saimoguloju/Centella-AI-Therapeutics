# orchestrator.py
"""Main Orchestrator Agent for the Virtual Screening System."""

import json
import pandas as pd
from typing import Any, Dict, Optional, List
from datetime import datetime
import logging

from agents.target_parser_agent import TargetParserAgent
from agents.library_generator_agent import LibraryGeneratorAgent
from agents.docking_agent import DockingAgent
from agents.ranking_agent import RankingAgent
from agents.summary_agent import SummaryAgent
from agents.knowledge_agent import KnowledgeAgent
from agents.memory_module import MemoryModule

logging.basicConfig(level=logging.INFO)


class OrchestratorAgent:
    """Main orchestrator that coordinates all sub-agents."""
    
    def __init__(self):
        """Initialize the orchestrator and all sub-agents."""
        self.logger = logging.getLogger("OrchestratorAgent")
        
        # Initialize all agents
        self.target_parser = TargetParserAgent()
        self.library_generator = LibraryGeneratorAgent()
        self.docking_agent = DockingAgent()
        self.ranking_agent = RankingAgent()
        self.summary_agent = SummaryAgent()
        self.knowledge_agent = KnowledgeAgent()
        self.memory = MemoryModule()
        
        self.logger.info("Orchestrator initialized with all agents")
    
    def process_query(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Process a user query through the appropriate workflow.
        
        Args:
            query: User query dictionary
            
        Returns:
            Dictionary with results
        """
        self.logger.info(f"Processing query: {query}")
        
        # Determine query type
        query_type = self._determine_query_type(query)
        
        if query_type == "knowledge":
            return self._handle_knowledge_query(query)
        elif query_type == "screening":
            return self._handle_screening_workflow(query)
        elif query_type == "memory":
            return self._handle_memory_operation(query)
        else:
            return {
                "error": "Unknown query type",
                "message": "Please specify a valid query type"
            }
    
    def _determine_query_type(self, query: Dict[str, Any]) -> str:
        """Determine the type of query.
        
        Args:
            query: User query
            
        Returns:
            Query type string
        """
        if 'question' in query:
            return "knowledge"
        elif 'memory_operation' in query:
            return "memory"
        elif 'target' in query or 'smiles_file' in query:
            return "screening"
        else:
            # Check if it's a continuation query
            if 'library_size' in query and self.memory.get_last_target():
                return "screening"
            return "unknown"
    
    def _handle_knowledge_query(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Handle knowledge-based queries.
        
        Args:
            query: Query with 'question' field
            
        Returns:
            Dictionary with answer
        """
        self.logger.info("Routing to Knowledge Agent")
        result = self.knowledge_agent.execute(query)
        
        # Update memory
        self.memory.update_context(query, result)
        
        return result
    
    def _handle_memory_operation(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Handle memory operations.
        
        Args:
            query: Query with memory operation
            
        Returns:
            Dictionary with memory operation result
        """
        self.logger.info("Handling memory operation")
        return self.memory.execute({
            'operation': query.get('memory_operation', 'get_context')
        })
    
    def _handle_screening_workflow(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Handle the main virtual screening workflow.
        
        Args:
            query: Screening query
            
        Returns:
            Dictionary with screening results
        """
        results = {}
        
        # Check memory for context
        if 'target' not in query and self.memory.get_last_target():
            query['target'] = self.memory.get_last_target()
            self.logger.info(f"Using target from memory: {query['target']}")
        
        if 'library_size' not in query and self.memory.get_last_library_size():
            query['library_size'] = self.memory.get_last_library_size()
            self.logger.info(f"Using library size from memory: {query['library_size']}")
        
        # Step 1: Parse target (if provided)
        if 'target' in query:
            self.logger.info("Step 1: Parsing target")
            target_result = self.target_parser.execute(query)
            
            if target_result.get('status') != 'success':
                return target_result
            
            results.update(target_result)
        
        # Step 2: Generate library (if not custom)
        if 'smiles_file' not in query:
            self.logger.info("Step 2: Generating molecular library")
            library_result = self.library_generator.execute(query)
            
            if library_result.get('status') != 'success':
                return library_result
            
            results['molecules'] = library_result['molecules']
            results['library_size'] = library_result['library_size']
        else:
            # Load custom SMILES file
            results['molecules'] = self._load_custom_smiles(query['smiles_file'])
            results['library_size'] = len(results['molecules'])
        
        # Step 3: Perform docking
        self.logger.info("Step 3: Performing molecular docking")
        docking_result = self.docking_agent.execute(results)
        
        if docking_result.get('status') != 'success':
            return docking_result
        
        results['docking_results'] = docking_result['docking_results']
        
        # Step 4: Rank molecules
        self.logger.info("Step 4: Ranking molecules")
        ranking_result = self.ranking_agent.execute(docking_result)
        
        if ranking_result.get('status') != 'success':
            return ranking_result
        
        results.update(ranking_result)
        
        # Step 5: Generate summary (unless skipped)
        if not query.get('skip_summary', False):
            self.logger.info("Step 5: Generating summary")
            summary_result = self.summary_agent.execute(results)
            
            if summary_result.get('status') == 'success':
                results['summary'] = summary_result['summary']
        
        # Save results to files
        self._save_results(results)
        
        # Update memory
        self.memory.update_context(query, results)
        
        return {
            "status": "success",
            "message": "Virtual screening completed successfully",
            "results": results,
            "files_generated": ["docking_results.csv", "top_hits.csv", "summary.md"]
        }
    
    def _load_custom_smiles(self, filename: str) -> List[Dict[str, str]]:
        """Load custom SMILES from file.
        
        Args:
            filename: Path to SMILES file
            
        Returns:
            List of molecules
        """
        molecules = []
        try:
            with open(filename, 'r') as f:
                for i, line in enumerate(f, 1):
                    smiles = line.strip()
                    if smiles:
                        molecules.append({
                            "ligand_id": f"L{i}",
                            "smiles": smiles
                        })
        except Exception as e:
            self.logger.error(f"Error loading SMILES file: {e}")
        
        return molecules
    
    def _save_results(self, results: Dict[str, Any]):
        """Save results to CSV and markdown files.
        
        Args:
            results: Dictionary with screening results
        """
        try:
            # Save docking results
            if 'docking_results' in results:
                df_docking = pd.DataFrame(results['docking_results'])
                df_docking.to_csv('docking_results.csv', index=False)
                self.logger.info("Saved docking_results.csv")
            
            # Save top hits
            if 'top_hits' in results:
                df_hits = pd.DataFrame(results['top_hits'])
                df_hits.to_csv('top_hits.csv', index=False)
                self.logger.info("Saved top_hits.csv")
            
            # Save summary
            if 'summary' in results:
                with open('summary.md', 'w') as f:
                    f.write(results['summary'])
                self.logger.info("Saved summary.md")
        
        except Exception as e:
            self.logger.error(f"Error saving results: {e}")


def main():
    """Main entry point for CLI usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Virtual Screening Orchestrator")
    parser.add_argument('--query', type=str, required=True,
                       help='JSON file containing the query')
    
    args = parser.parse_args()
    
    # Load query
    try:
        with open(args.query, 'r') as f:
            query = json.load(f)
    except Exception as e:
        print(f"Error loading query file: {e}")
        return
    
    # Initialize orchestrator
    orchestrator = OrchestratorAgent()
    
    # Process query
    results = orchestrator.process_query(query)
    
    # Print results
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
