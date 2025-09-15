# app.py
"""Streamlit interface for Virtual Screening System."""

import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import sys

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from orchestrator import OrchestratorAgent

# Page configuration
st.set_page_config(
    page_title="Virtual Screening System",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .main-header {
        text-align: center;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.9);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 5px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = OrchestratorAgent()

if 'results_history' not in st.session_state:
    st.session_state.results_history = []

if 'current_results' not in st.session_state:
    st.session_state.current_results = None

# Header
st.markdown("""
<div class="main-header">
    <h1>🧬 Virtual Screening System</h1>
    <p>AI-Powered Drug Discovery Pipeline</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🎯 Screening Configuration")
    
    # Mode selection
    mode = st.radio(
        "Select Mode",
        ["Virtual Screening", "Knowledge Query", "Memory Management"],
        help="Choose the operation mode"
    )
    
    st.divider()
    
    if mode == "Virtual Screening":
        # Target selection
        st.subheader("Target Protein")
        
        target_type = st.radio(
            "Input Type",
            ["Protein Name", "PDB ID", "Use Last Target"]
        )
        
        if target_type == "Protein Name":
            target = st.selectbox(
                "Select Protein",
                ["EGFR", "ACE2", "BRAF", "ALK", "CDK2", 
                 "VEGFR", "BCL2", "HSP90", "MTOR", "PI3K"]
            )
        elif target_type == "PDB ID":
            target = st.text_input("Enter PDB ID (4 characters)", "1A4G")
        else:
            target = None  # Will use memory
        
        # Library configuration
        st.subheader("Molecule Library")
        
        library_source = st.radio(
            "Library Source",
            ["Generate Random", "Custom SMILES"]
        )
        
        if library_source == "Generate Random":
            library_size = st.slider(
                "Library Size",
                min_value=5,
                max_value=30,
                value=20,
                step=5
            )
            custom_smiles = None
        else:
            custom_smiles = st.text_area(
                "Enter SMILES (one per line)",
                height=100,
                placeholder="CCO\nc1ccccc1\nCC(=O)O"
            )
            library_size = None
        
        # Advanced options
        with st.expander("Advanced Options"):
            top_n = st.slider("Top N Hits", 3, 10, 5)
            skip_summary = st.checkbox("Skip Summary Generation")
        
        # Run screening button
        if st.button("🚀 Run Virtual Screening", use_container_width=True):
            with st.spinner("Running virtual screening pipeline..."):
                # Prepare query
                query = {}
                if target:
                    query['target'] = target
                if library_size:
                    query['library_size'] = library_size
                if custom_smiles:
                    # Save custom SMILES to temp file
                    with open("temp_smiles.smi", "w") as f:
                        f.write(custom_smiles)
                    query['smiles_file'] = "temp_smiles.smi"
                query['top_n'] = top_n
                query['skip_summary'] = skip_summary
                
                # Process query
                result = st.session_state.orchestrator.process_query(query)
                st.session_state.current_results = result
                st.session_state.results_history.append(result)
    
    elif mode == "Knowledge Query":
        st.subheader("Ask a Chemistry Question")
        
        # Predefined questions
        example_questions = [
            "What is Lipinski's Rule of 5?",
            "What is ADMET?",
            "Explain molecular docking",
            "What is virtual screening?",
            "What is a pharmacophore?",
            "Explain QSAR",
            "What is lead optimization?",
            "What is bioavailability?"
        ]
        
        selected_question = st.selectbox(
            "Select a question or type your own",
            ["Custom Question"] + example_questions
        )
        
        if selected_question == "Custom Question":
            question = st.text_area(
                "Enter your question",
                height=100,
                placeholder="Ask about drug discovery concepts..."
            )
        else:
            question = selected_question
        
        if st.button("🔍 Get Answer", use_container_width=True):
            with st.spinner("Searching knowledge base..."):
                query = {"question": question}
                result = st.session_state.orchestrator.process_query(query)
                st.session_state.current_results = result
    
    else:  # Memory Management
        st.subheader("Memory Operations")
        
        # Show current memory context
        memory_context = st.session_state.orchestrator.memory.get_context()
        
        st.info(f"""
        **Current Session**
        - Last Target: {memory_context.get('last_target', 'None')}
        - Last Library Size: {memory_context.get('last_library_size', 'None')}
        - Queries Count: {memory_context.get('queries_count', 0)}
        """)
        
        if st.button("🧹 Clear Memory", use_container_width=True):
            query = {"memory_operation": "clear"}
            result = st.session_state.orchestrator.process_query(query)
            st.success("Memory cleared successfully!")
        
        if st.button("📊 Show Memory Context", use_container_width=True):
            query = {"memory_operation": "get_context"}
            result = st.session_state.orchestrator.process_query(query)
            st.session_state.current_results = result

# Main content area
if st.session_state.current_results:
    results = st.session_state.current_results
    
    if mode == "Virtual Screening" and results.get('status') == 'success':
        # Create tabs for different views
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Overview", "🏆 Top Hits", "📈 Visualizations", 
            "📄 Summary Report", "💾 Download Results"
        ])
        
        with tab1:
            st.header("Screening Overview")
            
            # Display metrics
            col1, col2, col3, col4 = st.columns(4)
            
            screening_data = results.get('results', {})
            
            with col1:
                st.metric(
                    "Target Protein",
                    screening_data.get('target_name', 'Unknown'),
                    screening_data.get('target_id', '')
                )
            
            with col2:
                st.metric(
                    "Library Size",
                    screening_data.get('library_size', 0)
                )
            
            with col3:
                best_score = screening_data.get('best_score', 0)
                st.metric(
                    "Best Docking Score",
                    f"{best_score:.2f}" if best_score else "N/A"
                )
            
            with col4:
                top_hits = screening_data.get('top_hits', [])
                st.metric(
                    "Promising Hits",
                    len([h for h in top_hits if h['docking_score'] < -7.0])
                )
        
        with tab2:
            st.header("Top Molecular Hits")
            
            top_hits = screening_data.get('top_hits', [])
            if top_hits:
                # Create DataFrame for display
                df_hits = pd.DataFrame(top_hits)
                
                # Style the dataframe
                st.dataframe(
                    df_hits,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "rank": st.column_config.NumberColumn("Rank", width="small"),
                        "ligand_id": st.column_config.TextColumn("Ligand ID"),
                        "smiles": st.column_config.TextColumn("SMILES Structure"),
                        "docking_score": st.column_config.NumberColumn(
                            "Docking Score",
                            format="%.2f",
                            help="Lower scores indicate better binding"
                        )
                    }
                )
                
                # Highlight best compound
                best_hit = top_hits[0]
                st.success(f"""
                🎯 **Lead Compound**: {best_hit['ligand_id']}
                - SMILES: `{best_hit['smiles']}`
                - Docking Score: {best_hit['docking_score']}
                """)
        
        with tab3:
            st.header("Data Visualizations")
            
            docking_results = screening_data.get('docking_results', [])
            
            if docking_results:
                df_all = pd.DataFrame(docking_results)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Score distribution
                    fig_hist = px.histogram(
                        df_all,
                        x='docking_score',
                        nbins=20,
                        title="Docking Score Distribution",
                        labels={'docking_score': 'Docking Score', 'count': 'Count'},
                        color_discrete_sequence=['#667eea']
                    )
                    st.plotly_chart(fig_hist, use_container_width=True)
                
                with col2:
                    # Top 10 compounds bar chart
                    df_top10 = df_all.nsmallest(10, 'docking_score')
                    fig_bar = px.bar(
                        df_top10,
                        x='ligand_id',
                        y='docking_score',
                        title="Top 10 Compounds",
                        labels={'docking_score': 'Docking Score', 'ligand_id': 'Ligand ID'},
                        color='docking_score',
                        color_continuous_scale='Viridis'
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
                
                # Score vs Compound scatter plot
                fig_scatter = go.Figure()
                
                # All compounds
                fig_scatter.add_trace(go.Scatter(
                    x=list(range(len(df_all))),
                    y=df_all['docking_score'].values,
                    mode='markers',
                    name='All Compounds',
                    marker=dict(color='lightblue', size=8)
                ))
                
                # Top hits
                top_indices = df_all.nsmallest(5, 'docking_score').index
                fig_scatter.add_trace(go.Scatter(
                    x=top_indices,
                    y=df_all.loc[top_indices, 'docking_score'].values,
                    mode='markers',
                    name='Top 5 Hits',
                    marker=dict(color='red', size=12, symbol='star')
                ))
                
                fig_scatter.update_layout(
                    title="Docking Scores Across All Compounds",
                    xaxis_title="Compound Index",
                    yaxis_title="Docking Score",
                    hovermode='closest'
                )
                
                st.plotly_chart(fig_scatter, use_container_width=True)
        
        with tab4:
            st.header("Summary Report")
            
            summary = screening_data.get('summary', '')
            if summary:
                st.markdown(summary)
            else:
                st.info("Summary generation was skipped")
        
        with tab5:
            st.header("Download Results")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Docking results CSV
                if 'docking_results' in screening_data:
                    df_docking = pd.DataFrame(screening_data['docking_results'])
                    csv_docking = df_docking.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Docking Results",
                        data=csv_docking,
                        file_name=f"docking_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
            
            with col2:
                # Top hits CSV
                if 'top_hits' in screening_data:
                    df_hits = pd.DataFrame(screening_data['top_hits'])
                    csv_hits = df_hits.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Top Hits",
                        data=csv_hits,
                        file_name=f"top_hits_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
            
            with col3:
                # Summary markdown
                if 'summary' in screening_data:
                    st.download_button(
                        label="📥 Download Summary",
                        data=screening_data['summary'],
                        file_name=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown"
                    )
    
    elif mode == "Knowledge Query":
        st.header("Knowledge Base Response")
        
        if 'answer' in results:
            st.markdown(results['answer'])
        else:
            st.error("No answer found")
    
    elif mode == "Memory Management":
        st.header("Memory Context")
        
        if 'context' in results:
            st.json(results['context'])
        else:
            st.info(results.get('message', 'Operation completed'))

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: rgba(255,255,255,0.7);'>
    <p>Virtual Screening System v1.0 | Built with Streamlit & LangChain</p>
    <p>For demonstration purposes only - Not for actual drug discovery</p>
</div>
""", unsafe_allow_html=True)
