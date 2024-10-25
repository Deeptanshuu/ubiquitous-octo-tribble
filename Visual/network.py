import pandas as pd
import plotly.graph_objects as go
import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load the dataset
data = pd.read_csv('7k-dataset-with-vectors.csv')

# Use the first 100 entries for visualization
data_subset = data.head(7500)

# Example user input
user_input = {
    "ingredients_name": ["chicken", "rice", "broccoli"]
}

# Create a dummy vector for user input (mean of ingredient vectors)
# In practice, you would create a proper TF-IDF vector from the user input.
user_vector = np.mean(data_subset['tfidf_vectors'].apply(lambda x: np.array(eval(x))), axis=0).reshape(1, -1)

# Calculate cosine similarity against the entire dataset
cosine_similarities = cosine_similarity(user_vector, np.stack(data['tfidf_vectors'].apply(lambda x: np.array(eval(x)))))[0]

# Create a DataFrame for similarities
similarity_df = pd.DataFrame({
    'name': data['name'],
    'similarity': cosine_similarities
})

# Get the top 100 matches with similarity greater than 0.1
top_matches = similarity_df[similarity_df['similarity'] > 0.1].nlargest(100, 'similarity')

# Create a graph
G = nx.Graph()

# Add nodes for top matches
for index, row in top_matches.iterrows():
    G.add_node(row['name'], similarity=row['similarity'])

# Add edges based on similarity
for i, row1 in top_matches.iterrows():
    for j, row2 in top_matches.iterrows():
        if i < j:  # Avoid duplicate edges
            G.add_edge(row1['name'], row2['name'])

# Get positions for nodes using a layout
pos = nx.spring_layout(G)

# Create edge traces
edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines'
)

# Create node traces
node_x = []
node_y = []
node_colors = []
node_sizes = []
for node, data in G.nodes(data=True):
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    if data.get('is_user_input', False):
        node_colors.append('blue')
        node_sizes.append(30)  # Make user input node larger
    else:
        node_colors.append(data['similarity'])
        node_sizes.append(10 + data['similarity'] * 20)  # Adjust size based on similarity

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers',
    hoverinfo='text',
    text=[f"{node}: {data['similarity']:.2f}" for node, data in G.nodes(data=True)],
    marker=dict(
        showscale=True,
        colorscale='YlOrRd',
        size=node_sizes,
        color=node_colors,
        colorbar=dict(title='Similarity'),
        line=dict(width=2)
    )
)

# Create the figure and plot
fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title='Recipe Similarity Network',
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
fig.show()
