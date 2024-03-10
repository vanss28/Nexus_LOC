import streamlit as st
import networkx as nx
import plotly.graph_objects as go
import numpy as np
import pandas as pd
d2 = pd.read_csv("articles.csv")
d3= pd.read_csv("articles2.csv")
ipo_cat_data = d2.groupby('Category').get_group('IPO') 
ipo = ipo_cat_data['Title']

ep_cat_data = d2.groupby('Category').get_group('Energy Policies and Renewable Energy') 
ep = ep_cat_data['Title']


gr_cat_data = d2.groupby('Category').get_group('Government Regulations and Policies')
gr = gr_cat_data['Title']

hp_cat_data = d2.groupby('Category').get_group('Healthcare Policies and Regulations')
hp = hp_cat_data['Title']

id_cat_data = d2.groupby('Category').get_group('Infrastructure Development and Investments')
idi = id_cat_data['Title']

esg_cat_data = d3.groupby('Category').get_group('Environmental, Social, and Governance (ESG) Investing') 
esg = esg_cat_data['Title']

mt_cat_data = d3.groupby('Category').get_group('Market Technology') 
mt = mt_cat_data['Title']


cc_cat_data = d3.groupby('Category').get_group('Climate Change and Market Impacts')
cc = cc_cat_data['Title']

p_cat_data = d3.groupby('Category').get_group('Pharma')
p = p_cat_data['Title']

au_cat_data = d3.groupby('Category').get_group('Automobiles')
au = au_cat_data['Title']

# Sample Data (Replace with your actual data)
data = {
    'IPO': ipo,
    'Energy Policies and Renewable Energy': ep,
    'Government Regulations and Policies': gr,
    'Healthcare Policies and Regulations': hp,
    'Infrastructure Development and Investments': idi,
    'Market Technology': mt,
    'Environmental, Social, and Governance (ESG) Investing': esg,
    'Climate Change and Market Impacts': cc,
    'Pharma': p,
    'Automobiles': au
}

def create_graph(selected_key):
    G = nx.DiGraph()
    fig = go.Figure()
    if selected_key == "All": 
        for key, titles in data.items():
            for title in titles:
                 G.add_node(title)  # Add the title as a node

        # Connect to head nodes if you want to preserve category association
                 if key in G:  # If the category head node already exists
                    G.add_edge(key, title, weight=1)
                 else:  # If not, create the head node
                     G.add_node(key)
                     G.add_edge(key, title, weight=1)
        # Create a graph using titles from all keys in the 'data' dictionary
        pos = nx.kamada_kawai_layout(G, weight='weight')
        plotly_pos = {node: np.array(pos[node]) for node in G.nodes()}

        # ... (Rest of the Plotly code for figure creation - same as before)
        

    # Add nodes
        fig.add_trace(go.Scatter(x=[pos[0] for pos in plotly_pos.values()],
                        y=[pos[1] for pos in plotly_pos.values()],
                        mode='markers',
                        text=list(G.nodes()),
                        textposition='bottom center',
                        marker=dict(size=50,color=['yellow' if node in data else 'blue' 
                                           for node in G.nodes()])
                         ))

    # Add edges
        for edge in G.edges:
                x0, y0 = plotly_pos[edge[0]]
                x1, y1 = plotly_pos[edge[1]]
                fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1],
                                    mode='lines',
                                    line=dict(color='black', width=2),
                                    hoverinfo='none')) 
        
    else:
        G.add_node(selected_key)  # Add the selected head node

        titles = data[selected_key]
        for title in titles:
            G.add_node(title)
            G.add_edge(selected_key, title, weight=3)

        pos = nx.kamada_kawai_layout(G, weight='weight')
        plotly_pos = {node: np.array(pos[node]) for node in G.nodes()}

        # ... (Rest of the Plotly code for figure creation - same as before)
        

    # Add nodes
        fig.add_trace(go.Scatter(x=[pos[0] for pos in plotly_pos.values()],
                        y=[pos[1] for pos in plotly_pos.values()],
                        mode='markers',
                        text=list(G.nodes()),
                        textposition='bottom center',
                        marker=dict(size=50,color=['yellow' if node in data else 'blue' 
                                           for node in G.nodes()])
                         ))

    # Add edges
        for edge in G.edges:
                x0, y0 = plotly_pos[edge[0]]
                x1, y1 = plotly_pos[edge[1]]
                fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1],
                                    mode='lines',
                                    line=dict(color='black', width=2),
                                    hoverinfo='none')) 

    # Customize layout 
    fig.update_layout(showlegend=False,
                    xaxis=dict(visible=False), yaxis=dict(visible=False))
    return fig

# Streamlit App
st.title("NetworkX Graph Visualization")

# User Input
selected_key = st.selectbox("Select a Data Key:", options=["All"] + list(data.keys()))


# Create and display the graph
if selected_key:  # Only create the graph if a key is selected
    graph_fig = create_graph(selected_key)
    st.plotly_chart(graph_fig)
