"""
    This script extracts the "about" column of the provided dataset.
    Empty entries and entries shorter than a threshold are removed.
    Then the remaining entries are stored in a separate CSV file.
"""

import pandas as pd

# Config
file_path = ""
minimum_bio_length = 256

if __name__ == "__main__":
    df = pd.read_csv(file_path, encoding="UTF-8")
    df = df["about"]
    df = df.dropna()
    df = df[df.map(len) >= minimum_bio_length]
    df.to_csv("bio_dataset.csv", encoding="UTF-8", index=False)
