# create_flow_diagram.py
"""Create a flow diagram for the Virtual Screening System."""

import plotly.graph_objects as go
import plotly.io as pio

def create_flow_diagram():
    """Create an interactive flow diagram of the system architecture."""
    
    # Define nodes
    nodes = [
        "User Interface",
        "Orchestrator Agent",
        "Target Parser",
        "Library Generator",
        "Docking Agent",
        "Ranking Agent",
        "Summary Agent",
        "Knowledge Agent",
        "Memory Module"
    ]
    
    # Define node positions
    positions = {
        "User Interface": (0.5, 1.0),
        "Orchestrator Agent": (0.5, 0.7),
        "Target Parser": (0.1, 0.4),
        "Library Generator": (0.25, 0.4),
        "Docking Agent": (0.4, 0.4),
        "Ranking Agent": (0.55, 0.4),
        "Summary Agent": (0.7, 0.4),
        "Knowledge Agent": (0.85, 0.4),
        "Memory Module": (0.5, 0.1)
    }
    
    # Create edges
    edges = [
        ("User Interface", "Orchestrator Agent"),
        ("Orchestrator Agent", "Target Parser"),
        ("Orchestrator Agent", "Library Generator"),
        ("Orchestrator Agent", "Docking Agent"),
        ("Orchestrator Agent", "Ranking Agent"),
        ("Orchestrator Agent", "Summary Agent"),
        ("Orchestrator Agent", "Knowledge Agent"),
        ("Orchestrator Agent", "Memory Module"),
        ("Target Parser", "Docking Agent"),
        ("Library Generator", "Docking Agent"),
        ("Docking Agent", "Ranking Agent"),
        ("Ranking Agent", "Summary Agent")
    ]
    
    # Create figure
    fig = go.Figure()
    
    # Add edges
    for edge in edges:
        x0, y0 = positions[edge[0]]
        x1, y1 = positions[edge[1]]
        
        fig.add_trace(go.Scatter(
            x=[x0, x1],
            y=[y0, y1],
            mode='lines',
            line=dict(color='rgba(150, 150, 150, 0.5)', width=2),
            hoverinfo='none',
            showlegend=False
        ))
    
    # Add nodes
    for node in nodes:
        x, y = positions[node]
        
        # Determine node color
        if node == "User Interface":
            color = '#667eea'
        elif node == "Orchestrator Agent":
            color = '#764ba2'
        elif node == "Memory Module":
            color = '#f093fb'
        else:
            color = '#4facfe'
        
        fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode='markers+text',
            marker=dict(
                size=40,
                color=color,
                line=dict(color='white', width=2)
            ),
            text=node,
            textposition='bottom center',
            textfont=dict(size=10, color='black'),
            hoverinfo='text',
            hovertext=f"<b>{node}</b>",
            showlegend=False
        ))
    
    # Update layout
    fig.update_layout(
        title={
            'text': "Virtual Screening System Architecture",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#333'}
        },
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-0.1, 1.1]
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-0.1, 1.1]
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=600,
        width=900,
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    # Add annotations for workflow stages
    annotations = [
        dict(
            x=0.5, y=0.85,
            text="Input Processing",
            showarrow=False,
            font=dict(size=12, color='gray', style='italic')
        ),
        dict(
            x=0.5, y=0.55,
            text="Agent Orchestration",
            showarrow=False,
            font=dict(size=12, color='gray', style='italic')
        ),
        dict(
            x=0.425, y=0.25,
            text="Screening Pipeline",
            showarrow=False,
            font=dict(size=12, color='gray', style='italic')
        ),
        dict(
            x=0.85, y=0.25,
            text="Knowledge Base",
            showarrow=False,
            font=dict(size=12, color='gray', style='italic')
        ),
        dict(
            x=0.5, y=-0.05,
            text="Persistence Layer",
            showarrow=False,
            font=dict(size=12, color='gray', style='italic')
        )
    ]
    
    fig.update_layout(annotations=annotations)
    
    return fig


def save_diagram():
    """Save the flow diagram as HTML and PNG."""
    fig = create_flow_diagram()
    
    # Save as interactive HTML
    fig.write_html("flow_diagram.html")
    print("✅ Saved flow_diagram.html")
    
    # Save as static image (requires kaleido)
    try:
        fig.write_image("flow_diagram.png", width=1200, height=800, scale=2)
        print("✅ Saved flow_diagram.png")
    except:
        print("⚠️  Could not save PNG (install kaleido: pip install kaleido)")
    
    # Show the figure
    fig.show()


if __name__ == "__main__":
    save_diagram()
