import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle
import os

DATA_PATH = "data/processed/shl_clean.csv"
INDEX_PATH = "embeddings/shl_faiss.index"
META_PATH = "embeddings/metadata.pkl"

def main():
    df = pd.read_csv(DATA_PATH)

    texts = df["combined_text"].tolist()

    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Creating embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True)

    embeddings = np.array(embeddings).astype("float32")

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    os.makedirs("embeddings", exist_ok=True)
    faiss.write_index(index, INDEX_PATH)

    with open(META_PATH, "wb") as f:
        pickle.dump(df.to_dict(orient="records"), f)

    print("FAISS index created")
    print("Total vectors:", index.ntotal)

if __name__ == "__main__":
    main()
