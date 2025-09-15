# agents/knowledge_agent.py
"""Knowledge Agent for answering chemistry and pharmaceutical questions."""

from typing import Any, Dict
from .base_agent import BaseAgent


class KnowledgeAgent(BaseAgent):
    """Agent responsible for answering domain-specific questions."""
    
    def __init__(self):
        super().__init__(
            name="KnowledgeAgent",
            description="Answers chemistry and pharmaceutical questions from knowledge base"
        )
        
        # Initialize knowledge base
        self.knowledge_base = self._initialize_knowledge_base()
    
    def _initialize_knowledge_base(self) -> Dict[str, str]:
        """Initialize the knowledge base with chemistry/pharma information."""
        return {
            "lipinski": """**Lipinski's Rule of 5** is a set of guidelines to evaluate drug-likeness:
1. Molecular weight < 500 Da
2. LogP (lipophilicity) < 5
3. Hydrogen bond donors ≤ 5
4. Hydrogen bond acceptors ≤ 10

These rules help predict oral bioavailability of drug candidates.""",
            
            "admet": """**ADMET** stands for:
- **A**bsorption: How the drug enters the bloodstream
- **D**istribution: How the drug spreads throughout the body
- **M**etabolism: How the drug is broken down
- **E**xcretion: How the drug is eliminated from the body
- **T**oxicity: Harmful effects of the drug

ADMET studies are crucial for drug development to ensure safety and efficacy.""",
            
            "docking": """**Molecular Docking** is a computational technique used to predict:
- How small molecules (ligands) bind to proteins (targets)
- Binding affinity and orientation
- Key interactions between ligand and protein

Docking scores (typically negative values) indicate binding strength - lower scores mean stronger binding.""",
            
            "virtual_screening": """**Virtual Screening** is a computational approach to:
- Screen large libraries of compounds
- Identify potential drug candidates
- Reduce time and cost of drug discovery
- Prioritize compounds for experimental testing

It combines various techniques including docking, ADMET prediction, and machine learning.""",
            
            "pharmacophore": """**Pharmacophore** is the ensemble of steric and electronic features necessary for:
- Optimal molecular recognition by a biological target
- Triggering or blocking biological response
- Includes features like hydrogen bond donors/acceptors, aromatic rings, hydrophobic regions""",
            
            "qsar": """**QSAR (Quantitative Structure-Activity Relationship)** models:
- Correlate chemical structure with biological activity
- Predict activity of new compounds
- Guide lead optimization
- Use molecular descriptors and machine learning""",
            
            "lead_optimization": """**Lead Optimization** involves:
- Improving potency and selectivity
- Enhancing ADMET properties
- Reducing toxicity
- Maintaining drug-like properties
- Structure-Activity Relationship (SAR) studies""",
            
            "high_throughput_screening": """**High-Throughput Screening (HTS)**:
- Automated testing of thousands to millions of compounds
- Identifies active compounds (hits)
- Uses robotics and data processing
- Complementary to virtual screening""",
            
            "drug_target": """**Drug Targets** are biological molecules that drugs interact with:
- Proteins (enzymes, receptors, ion channels)
- Nucleic acids (DNA, RNA)
- Carbohydrates
- Lipids

Most drugs target proteins, especially G-protein coupled receptors (GPCRs) and kinases.""",
            
            "bioavailability": """**Bioavailability** is the fraction of administered drug that reaches systemic circulation:
- Affected by absorption, first-pass metabolism
- Oral bioavailability often < 100%
- IV administration = 100% bioavailability
- Critical for drug dosing""",
        }
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Answer a chemistry/pharma question.
        
        Args:
            input_data: Dictionary containing 'question' field
            
        Returns:
            Dictionary with answer
        """
        if not self.validate_input(input_data, ['question']):
            return {"error": "Missing question field"}
        
        question = input_data['question'].lower()
        self.log_execution(f"Answering question: {question}")
        
        # Find relevant answer
        answer = self._find_answer(question)
        
        return {
            "question": input_data['question'],
            "answer": answer,
            "status": "success"
        }
    
    def _find_answer(self, question: str) -> str:
        """Find answer from knowledge base.
        
        Args:
            question: User's question (lowercase)
            
        Returns:
            Answer string
        """
        # Check for keywords in question
        keywords_map = {
            "lipinski": ["lipinski", "rule of 5", "rule of five", "ro5"],
            "admet": ["admet", "absorption", "distribution", "metabolism", "excretion", "toxicity"],
            "docking": ["docking", "binding score", "docking score"],
            "virtual_screening": ["virtual screening", "computational screening"],
            "pharmacophore": ["pharmacophore"],
            "qsar": ["qsar", "structure activity", "structure-activity"],
            "lead_optimization": ["lead optimization", "lead optimisation"],
            "high_throughput_screening": ["hts", "high throughput", "high-throughput"],
            "drug_target": ["drug target", "target", "protein target"],
            "bioavailability": ["bioavailability", "bioavailable"],
        }
        
        for key, keywords in keywords_map.items():
            if any(kw in question for kw in keywords):
                return self.knowledge_base[key]
        
        # Default response
        return """I don't have specific information about that topic in my knowledge base. 
        
Available topics include:
- Lipinski's Rule of 5
- ADMET properties
- Molecular Docking
- Virtual Screening
- Pharmacophore modeling
- QSAR
- Lead Optimization
- High-Throughput Screening
- Drug Targets
- Bioavailability

Please ask about one of these topics for detailed information."""
