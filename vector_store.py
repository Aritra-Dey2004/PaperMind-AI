import faiss  # type: ignore[import]
import numpy as np  # type: ignore[import]

def create_faiss_index(embeddings):
    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    return index