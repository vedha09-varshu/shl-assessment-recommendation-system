import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from retriever.search import search_assessments

K = 10
TRAIN_PATH = "data/train/train.csv"

def recall_at_k(predicted_urls, true_urls, k=10):
    predicted_urls = predicted_urls[:k]
    hits = len(set(predicted_urls) & set(true_urls))
    return hits / len(true_urls) if true_urls else 0

def main():
    df = pd.read_csv(TRAIN_PATH)

    scores = []

    for query, group in df.groupby("Query"):
        true_urls = group["Assessment_url"].tolist()

        results = search_assessments(query, top_k=K)
        predicted_urls = [r["url"] for r in results]

        score = recall_at_k(predicted_urls, true_urls, K)
        scores.append(score)

        print(f"Query: {query}")
        print(f"Recall@{K}: {score:.2f}")
        print("-" * 40)

    mean_recall = sum(scores) / len(scores)
    print(f"\n Mean Recall@{K}: {mean_recall:.2f}")

if __name__ == "__main__":
    main()
