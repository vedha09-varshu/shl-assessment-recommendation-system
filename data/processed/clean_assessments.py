import pandas as pd
import re

INPUT_PATH = "data/raw/shl_assessments.csv"
OUTPUT_PATH = "data/processed/shl_clean.csv"

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-z0-9,. ]", "", text)
    return text.strip()

def main():
    df = pd.read_csv(INPUT_PATH)

    df["name_clean"] = df["name"].apply(clean_text)
    df["description_clean"] = df["description"].apply(clean_text)

    # combined_text is GENERATED here
    df["combined_text"] = df["name_clean"] + ". " + df["description_clean"]

    df = df[["name", "url", "description", "test_type", "combined_text"]]

    df.to_csv(OUTPUT_PATH, index=False)

    print(" Clean file created")
    print("Columns:", df.columns.tolist())
    print("Rows:", len(df))

if __name__ == "__main__":
    main()
