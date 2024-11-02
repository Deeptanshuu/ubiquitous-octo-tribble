import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import plotly.graph_objects as go
from tqdm import tqdm
import concurrent.futures
import multiprocessing
from joblib import Memory
import umap.umap_ as umap

# Set up caching
memory = Memory("./cache_dir", verbose=0)

# Function to process TF-IDF vectors
@memory.cache
def process_tfidf_vector(vector_str):
    return np.array(eval(vector_str))

# Function to calculate cosine similarity
def calculate_similarity(user_vector, recipe_vector):
    return cosine_similarity(user_vector.reshape(1, -1), recipe_vector.reshape(1, -1))[0][0]

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

# Calculate similarities
print("Calculating similarities...")
with concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
    similarities = list(tqdm(executor.map(lambda x: calculate_similarity(user_vector, x), df['tfidf_vectors']), total=len(df)))
df['similarity'] = similarities

# Get top and bottom recipes
top_30 = df.sort_values(by="similarity", ascending=False).head(10)
bottom_30 = df.sort_values(by="similarity", ascending=True).head(10)

# Apply UMAP for dimensionality reduction
print("Applying UMAP...")
reducer = umap.UMAP(n_components=3, 
                   random_state=42, 
                   n_neighbors=15,
                   min_dist=0.1,
                   metric='cosine')  # Using cosine distance since we're working with TF-IDF
all_vectors = np.vstack([np.vstack(df['tfidf_vectors']), user_vector])
transformed_vectors = reducer.fit_transform(all_vectors)

# Separate recipe vectors and user vector
recipes_3d = transformed_vectors[:-1]
user_vector_3d = transformed_vectors[-1]

# Create the 3D plot
print("Generating plot...")
fig = go.Figure()

# Function to create arrow
def create_arrow(start, end, color, opacity=1):
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
        sizeref=0.8,
        opacity=opacity
    )

# Plot top recipes
for i, idx in enumerate(top_30.index):
    recipe_name = df.loc[idx, 'name']
    end_point = recipes_3d[idx]
    fig.add_trace(go.Scatter3d(
        x=[0, end_point[0]],
        y=[0, end_point[1]],
        z=[0, end_point[2]],
        mode='lines',
        line=dict(color= 'green', width=3),  # Semi-transparent green
        name=f"Top {i+1}: {recipe_name}",
        showlegend=True
    ))
    arrow_end = [0.90 * coord for coord in end_point]
    fig.add_trace(create_arrow(arrow_end, end_point, 'green'))

# Plot bottom recipes
for i, idx in enumerate(bottom_30.index):
    recipe_name = df.loc[idx, 'name']
    end_point = recipes_3d[idx]
    fig.add_trace(go.Scatter3d(
        x=[0, end_point[0]],
        y=[0, end_point[1]],
        z=[0, end_point[2]],
        mode='lines',
        line=dict(color= 'red', width=3),  # Semi-transparent red
        name=f"Bottom {i+1}: {recipe_name}",
        showlegend=True
    ))
    arrow_end = [0.90 * coord for coord in end_point]
    fig.add_trace(create_arrow(arrow_end, end_point, 'red'))

# Plot user vector
fig.add_trace(go.Scatter3d(
    x=[0, user_vector_3d[0]],
    y=[0, user_vector_3d[1]],
    z=[0, user_vector_3d[2]],
    mode='lines',
    line=dict(color='blue', width=6),
    name='User Input Vector: ' + str(user_input_ingredients)
))
user_arrow_end = [0.90 * coord for coord in user_vector_3d]
fig.add_trace(create_arrow(user_arrow_end, user_vector_3d, 'blue'))

# Customize layout
fig.update_layout(
    scene=dict(
        xaxis_title='UMAP Component 1',
        yaxis_title='UMAP Component 2',
        zaxis_title='UMAP Component 3',
        aspectmode='cube'
    ),
    title='UMAP 3D Visualization of Recipe Vectors',
    showlegend=True,
)

# Show the plot
fig.show() 