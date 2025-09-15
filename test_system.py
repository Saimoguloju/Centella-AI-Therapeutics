# test_system.py
"""Test script to demonstrate Virtual Screening System capabilities."""

import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from orchestrator import OrchestratorAgent
import pandas as pd


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def test_screening_workflow():
    """Test the main virtual screening workflow."""
    print_section("TEST 1: Virtual Screening Workflow")
    
    orchestrator = OrchestratorAgent()
    
    # Test query
    query = {
        "target": "EGFR",
        "library_size": 10
    }
    
    print(f"Query: {json.dumps(query, indent=2)}")
    print("\nProcessing...")
    
    result = orchestrator.process_query(query)
    
    if result.get('status') == 'success':
        print("✅ Screening completed successfully!")
        
        # Display results
        results_data = result.get('results', {})
        print(f"\nTarget: {results_data.get('target_name')} ({results_data.get('target_id')})")
        print(f"Library Size: {results_data.get('library_size')}")
        print(f"Best Score: {results_data.get('best_score')}")
        
        # Show top hits
        top_hits = results_data.get('top_hits', [])[:3]
        if top_hits:
            print("\nTop 3 Hits:")
            for hit in top_hits:
                print(f"  - {hit['ligand_id']}: {hit['smiles']} (Score: {hit['docking_score']})")
    else:
        print(f"❌ Error: {result.get('error')}")


def test_knowledge_query():
    """Test the knowledge agent."""
    print_section("TEST 2: Knowledge Query")
    
    orchestrator = OrchestratorAgent()
    
    queries = [
        "What is Lipinski's Rule of 5?",
        "What is ADMET?",
        "Explain molecular docking"
    ]
    
    for query_text in queries:
        print(f"\nQuestion: {query_text}")
        print("-" * 40)
        
        result = orchestrator.process_query({"question": query_text})
        
        if 'answer' in result:
            # Print first 200 characters of answer
            answer = result['answer']
            if len(answer) > 200:
                print(answer[:200] + "...")
            else:
                print(answer)
        else:
            print("No answer found")


def test_memory_persistence():
    """Test memory module functionality."""
    print_section("TEST 3: Memory Persistence")
    
    orchestrator = OrchestratorAgent()
    
    # First query with target
    query1 = {
        "target": "BRAF",
        "library_size": 15
    }
    
    print("Query 1 (with target):")
    print(json.dumps(query1, indent=2))
    
    result1 = orchestrator.process_query(query1)
    print(f"✅ First query processed")
    
    # Second query without target (should use memory)
    query2 = {
        "library_size": 25
    }
    
    print("\nQuery 2 (without target - should use memory):")
    print(json.dumps(query2, indent=2))
    
    result2 = orchestrator.process_query(query2)
    
    if result2.get('status') == 'success':
        results_data = result2.get('results', {})
        remembered_target = results_data.get('target_name')
        print(f"✅ Memory worked! Used target: {remembered_target}")
    else:
        print("❌ Memory test failed")
    
    # Check memory context
    memory_context = orchestrator.memory.get_context()
    print(f"\nMemory Context:")
    print(f"  - Last Target: {memory_context.get('last_target')}")
    print(f"  - Last Library Size: {memory_context.get('last_library_size')}")
    print(f"  - Queries Count: {memory_context.get('queries_count')}")


def test_adaptive_workflow():
    """Test adaptive workflow with custom SMILES."""
    print_section("TEST 4: Adaptive Workflow")
    
    orchestrator = OrchestratorAgent()
    
    # Create a custom SMILES file
    custom_smiles = ["CCO", "c1ccccc1", "CC(=O)O", "CC(C)O", "c1ccc(O)cc1"]
    with open("test_custom.smi", "w") as f:
        for smiles in custom_smiles:
            f.write(f"{smiles}\n")
    
    # Query with custom SMILES and skip summary
    query = {
        "target": "ACE2",
        "smiles_file": "test_custom.smi",
        "skip_summary": True
    }
    
    print(f"Query: {json.dumps(query, indent=2)}")
    print("\nProcessing with custom SMILES...")
    
    result = orchestrator.process_query(query)
    
    if result.get('status') == 'success':
        print("✅ Adaptive workflow completed!")
        print("   - Used custom SMILES file")
        print("   - Skipped summary generation")
        
        results_data = result.get('results', {})
        print(f"   - Processed {results_data.get('library_size')} molecules")
    else:
        print(f"❌ Error: {result.get('error')}")
    
    # Clean up
    if os.path.exists("test_custom.smi"):
        os.remove("test_custom.smi")


def main():
    """Run all tests."""
    print("\n" + "🧬"*30)
    print("  VIRTUAL SCREENING SYSTEM - TEST SUITE")
    print("🧬"*30)
    
    tests = [
        test_screening_workflow,
        test_knowledge_query,
        test_memory_persistence,
        test_adaptive_workflow
    ]
    
    for test_func in tests:
        try:
            test_func()
        except Exception as e:
            print(f"\n❌ Test failed with error: {e}")
    
    print_section("TEST SUITE COMPLETED")
    print("\n✨ All tests completed! Check the generated files:")
    print("  - docking_results.csv")
    print("  - top_hits.csv")
    print("  - summary.md")
    print("  - session_memory.json")


if __name__ == "__main__":
    main()
