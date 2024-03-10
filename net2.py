import streamlit as st
import networkx as nx
import plotly.graph_objects as go
import numpy as np
import pandas as pd
data = pd.read_csv("Stock_Sector_Mapping.csv")
data.head()

finance_sector_data = data.groupby('Sector').get_group('Finance')

# Display result (you can also perform other operations on the filtered data)
fin = finance_sector_data['Name']
technology_sector_data = data[data['Sector'].str.lower().isin(
    ['it enabled services - software', 'technology services']
)]

# Display result (you can also modify this as needed)
tech = technology_sector_data['Name']

health_sector_data = data[data['Sector'].isin(
    ['Healthcare  - Facilities', 'Healthcare  - Supplies','MEDICAL EQUIPMENT & SUPPLIES','Storage Media & Peripherals']
)]

health = health_sector_data['Name']



# Sample Data
sectors = ["Technology Services", "Finance", "Healthcare"]
finance_stocks = fin
health_stocks = health
technology_stocks = tech
news_headline = st.text_input("Enter a News Headline:", "Tech Sector Surges on AI News")
selected_sector = st.selectbox("Select a Sector:", ["All"] + sectors)



# Create NetworkX graph 
G = nx.DiGraph()

# Add news headline 
G.add_node(news_headline)
if selected_sector == "All":
# Add sectors 
    for sector in sectors:
        G.add_node(sector)
        G.add_edge(news_headline, sector)

    # Add finance stocks and connect  
    for stock in finance_stocks:
        G.add_node(stock)
        G.add_edge("Finance", stock)

    for stock in health_stocks:
        G.add_node(stock)
        G.add_edge("Healthcare", stock)
        
    for stock in technology_stocks:
        G.add_node(stock)
        G.add_edge("Technology Services", stock)
# Layout 
else:
    G.add_node(selected_sector)
    G.add_edge(news_headline, selected_sector)
    if selected_sector == "Finance":
        for stock in finance_stocks: 
            G.add_node(stock)
            G.add_edge(selected_sector, stock)
    elif selected_sector == "Technology Services":
        for stock in technology_stocks: 
            G.add_node(stock)
            G.add_edge(selected_sector, stock)
    elif selected_sector == "Healthcare":
        for stock in health_stocks: 
            G.add_node(stock)
            G.add_edge(selected_sector, stock)
pos = nx.kamada_kawai_layout(G, scale=10,weight='weight')  # Adjust 'k' and 'seed' if needed 

# Convert positions for Plotly
plotly_pos = {node: np.array(pos[node]) for node in G.nodes()}
st.title("NetworkX Graph Visualization")
# Create Plotly figure
fig = go.Figure()

# Add nodes
fig.add_trace(go.Scatter(x=[pos[0] for pos in plotly_pos.values()],
                         y=[pos[1] for pos in plotly_pos.values()],
                         mode='markers',
                         text=list(G.nodes()),
                         textposition='bottom center',
                         marker=dict(size=50) 
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

st.plotly_chart(fig)

