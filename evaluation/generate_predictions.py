import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from retriever.search import search_assessments

TEST_PATH = "data/test/test.csv"
OUTPUT_PATH = "final_predictions.csv"

def main():
    df = pd.read_csv(TEST_PATH)

    rows = []

    for query in df["Query"]:
        results = search_assessments(query, top_k=10)

        for r in results:
            rows.append({
                "Query": query,
                "Assessment_url": r["url"]
            })

    out_df = pd.DataFrame(rows)
    out_df.to_csv(OUTPUT_PATH, index=False)

    print(" final_predictions.csv created")

if __name__ == "__main__":
    main()
