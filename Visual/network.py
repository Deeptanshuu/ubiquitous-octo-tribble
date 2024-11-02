import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.manifold import TSNE
import plotly.graph_objects as go
from tqdm import tqdm
import concurrent.futures
import multiprocessing
from joblib import Memory

# Set up caching
memory = Memory("./cache_dir", verbose=0)

# Function to process TF-IDF vectors
@memory.cache
def process_tfidf_vector(vector_str):
    return np.array(eval(vector_str))

# Function to calculate cosine similarity
def calculate_similarity(user_vector, recipe_vector):
    return cosine_similarity(user_vector.reshape(1, -1), recipe_vector.reshape(1, -1))[0][0]

# Cached t-SNE function
@memory.cache
def cached_tsne(vectors):
    tsne = TSNE(n_components=3, random_state=42, verbose=1, max_iter=1000)
    return tsne.fit_transform(vectors)

# Load the dataset
print("Loading dataset...")
df = pd.read_csv("7k-dataset-with-vectors.csv")

# Limit to the first 7500 recipes
df = df.head(7541)

# Convert 'tfidf_vectors' column from string to numpy array using multithreading
print("Processing TF-IDF vectors...")
with concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
    df['tfidf_vectors'] = list(tqdm(executor.map(process_tfidf_vector, df['tfidf_vectors']), total=len(df)))

# Generate user ingredient vector
user_input_ingredients = ["chicken", "rice", "onion", "red chili", "egg noodles", "rice noodles", "ginger", "tomatoes"]
#user_input_ingredients = ["sugar", "chocolate", "vanilla extract", "baking soda", "eggs", "cocoa powder"]
user_vector = np.zeros(df['tfidf_vectors'].iloc[0].shape)
for ingredient in user_input_ingredients:
    matching_recipes = df[df['ingredients_text'].str.contains(ingredient, case=False, na=False)]
    if not matching_recipes.empty:
        user_vector += np.mean(np.vstack(matching_recipes['tfidf_vectors']), axis=0)

# Normalize user vector only if it's not all zeros
if np.any(user_vector):
    user_vector = user_vector / np.linalg.norm(user_vector)

# Combine user vector with recipe vectors for t-SNE
all_vectors = np.vstack([np.vstack(df['tfidf_vectors']), user_vector])

# Apply t-SNE to all vectors including the user vector
print("Reducing dimensions for all vectors...")
all_vectors_3d = cached_tsne(all_vectors)

# Separate the user vector and recipe vectors
user_vector_3d = all_vectors_3d[-1]
recipes_3d = all_vectors_3d[:-1]

# Step 3: Calculate cosine similarities using multithreading
print("Calculating similarities...")
with concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
    similarities = list(tqdm(executor.map(lambda x: calculate_similarity(user_vector, x), df['tfidf_vectors']), total=len(df)))
df['similarity'] = similarities

# Get top 10 similar recipes
top_10 = df.sort_values(by="similarity", ascending=False).head(10)
bottom_10 = df.sort_values(by="similarity", ascending=True).head(10)

# Prepare data for plotting
top_10_indices = top_10.index
bottom_10_indices = bottom_10.index

# Step 4: Plot the 3D vector space using Plotly
print("Generating plot...")
fig = go.Figure()

# Function to create arrow
def create_arrow(start, end, color):
    return go.Cone(
        x=[end[0]],
        y=[end[1]],
        z=[end[2]],
        u=[end[0] - start[0]],
        v=[end[1] - start[1]],
        w=[end[2] - start[2]],
        colorscale=[[0, color], [1, color]],
        showscale=False,
        sizemode="absolute",
        sizeref=1.3  # Significantly increased size
    )

# Add top 10 recipe points as vectors originating from the origin (0, 0, 0) in green
for i, idx in enumerate(top_10_indices):
    recipe_name = df.loc[idx, 'name']  # Get recipe name
    end_point = recipes_3d[idx]
    fig.add_trace(go.Scatter3d(
        x=[0, end_point[0]],  # Start from origin
        y=[0, end_point[1]],  # Start from origin
        z=[0, end_point[2]],  # Start from origin
        mode='lines',
        line=dict(color='green', width=3),  # Use green for top 10 recipe vectors
        name=f"Top {i+1}: {recipe_name}",  # Set the trace name to include ranking
        showlegend=True  # Show legend for individual vectors
    ))
    # Add arrow at 90% of the vector length
    arrow_end = [0.90 * coord for coord in end_point]
    fig.add_trace(create_arrow(arrow_end, end_point, 'green'))

# Add bottom 10 recipe points as vectors originating from the origin (0, 0, 0) in red
for i, idx in enumerate(bottom_10_indices):
    recipe_name = df.loc[idx, 'name']  # Get recipe name using the correct index
    end_point = recipes_3d[idx]
    fig.add_trace(go.Scatter3d(
        x=[0, end_point[0]],  # Start from origin
        y=[0, end_point[1]],  # Start from origin
        z=[0, end_point[2]],  # Start from origin
        mode='lines',
        line=dict(color='red', width=3),  # Use red for bottom 10 recipe vectors
        name=f"Bottom {i+1}: {recipe_name}",  # Set the trace name to include ranking
        showlegend=True  # Show legend for individual vectors
    ))
    # Add arrow at 90% of the vector length
    arrow_end = [0.90 * coord for coord in end_point]
    fig.add_trace(create_arrow(arrow_end, end_point, 'red'))

# Plot user vector as an arrow in blue
user_end_point = user_vector_3d
fig.add_trace(go.Scatter3d(
    x=[0, user_end_point[0]],
    y=[0, user_end_point[1]],
    z=[0, user_end_point[2]],
    mode='lines',
    line=dict(color='orange', width=6),
    name='User Input Vector' +str(user_input_ingredients) # Keep the label for the user vector
))
# Add arrow at 90% of the vector length
user_arrow_end = [0.90 * coord for coord in user_end_point]
fig.add_trace(create_arrow(user_arrow_end, user_end_point, 'blue'))

# Customize the layout
fig.update_layout(
    scene=dict(
        xaxis_title='Dimension 1',
        yaxis_title='Dimension 2',
        zaxis_title='Dimension 3',
        aspectmode='auto'
    ),
    title='3D Visualization of Recipe Similarities',
    showlegend=True,  # Show legend for all vectors
    legend=dict(itemsizing='constant', font=dict(size=10))  # Adjust legend appearance
)

# Show the plot
fig.show()
