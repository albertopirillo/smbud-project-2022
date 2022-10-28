"""
  In this script the whole dataset is cleaned, reduced and converted to the CSV format.
  If the script crashes due to memory errors, lower the chunk_size and try again.
"""

# Uncomment if using Colab and if the dataset is stored on Google Drive
# from google.colab import drive
# drive.mount('/content/drive')

import pandas as pd
import numpy as np

# Config
file_path = ""
out_file_path = ""
chunk_size = 100_000
citation_thresh = 10
references_thresh = 10

# Structure of the columns of the dataset
col_labels = ("id", "title", "authors", "venue", "year", "n_citation", "page_start", "page_end", "doc_type",
              "publisher", "volume", "issue", "fos", "doi", "references", "abstract")

if __name__ == "__main__":
    df = pd.DataFrame()

    with pd.read_json(file_path, encoding="UTF-8", lines=True, chunksize=chunk_size) as reader:
        block_count = 0
        for chunk in reader:
            block_count += chunk_size
            df = chunk
            print(f"Blocks read: {block_count}")

            # Drop null and NaN values
            df = df.dropna(axis=0, how="any")

            # Drop papers with empty strings as fields
            for column in df:
                df = df[df[column] != ""]

            # Drop papers with low n_citation
            df = df[df["n_citation"] >= citation_thresh]

            # Drop papers with low references count
            num_references = df["references"].to_numpy().copy()
            for i in range(num_references.size):
                num_references[i] = len(num_references[i])
            df = df[num_references >= references_thresh]

            # Reconstruct abstract field and rename its column
            indexed_abstract = df["indexed_abstract"].to_numpy()
            for i in range(indexed_abstract.size):
                entry = indexed_abstract[i]
                string_arr = np.ndarray(shape=entry["IndexLength"], dtype=object)
                dictionary = entry["InvertedIndex"]
                for key, value in dictionary.items():
                    to_be_removed = {'\n', '\r', '\\'}
                    for char in to_be_removed:
                        key = key.replace(char, "")
                    for elem in value:
                        string_arr[elem] = key
                string_arr = string_arr[string_arr != None]
                indexed_abstract[i] = " ".join(string_arr)
            df = df.rename({"indexed_abstract": "abstract"}, axis=1)

            # Store the chunk in the .csv file
            if block_count == chunk_size:
                df.to_csv(out_file_path, encoding="UTF-8", index=False, mode="a",
                          header=True, escapechar="|", columns=col_labels)
            else:
                df.to_csv(out_file_path, encoding="UTF-8", index=False, mode="a",
                          header=False, escapechar="|", columns=col_labels)

    print("Conversion complete.")
