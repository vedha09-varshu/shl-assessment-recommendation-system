import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

INDEX_PATH = "embeddings/shl_faiss.index"
META_PATH = "embeddings/metadata.pkl"

model = SentenceTransformer("all-MiniLM-L6-v2")

def search_assessments(query, top_k=6):
    index = faiss.read_index(INDEX_PATH)

    with open(META_PATH, "rb") as f:
        metadata = pickle.load(f)

    query_embedding = model.encode([query]).astype("float32")
    distances, indices = index.search(query_embedding, 10)

    tech = []
    behavior = []

    for idx in indices[0]:
        if idx >= len(metadata):
            continue

        item = metadata[idx]
        test_type = item.get("test_type", "")

        if "Knowledge" in test_type:
            tech.append(item)
        elif "Personality" in test_type:
            behavior.append(item)

    # Balanced output
    results = []
    results.extend(tech[:top_k // 2])
    results.extend(behavior[:top_k // 2])

    # Fallback if one category is missing
    if len(results) < top_k:
        remaining = [x for x in metadata if x not in results]
        results.extend(remaining[: top_k - len(results)])

    return results

if __name__ == "__main__":
    query = "Need a Java developer who collaborates with business teams"
    results = search_assessments(query)

    for r in results:
        print(r["name"], " | ", r["test_type"])
