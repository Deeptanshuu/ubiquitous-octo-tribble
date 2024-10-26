# first line: 24
@memory.cache
def cached_tsne(vectors):
    tsne = TSNE(n_components=3, random_state=42, verbose=1)
    return tsne.fit_transform(vectors)
