"""
  In this script the whole dataset is cleaned and reduced in size.
  It takes as input a dataset stored in the JSON format and outputs a dataset stored in the CSV format.
  If the script crashes due to memory errors, lower the chunk_size and retry.
"""

import numpy as np
import pandas as pd

# Config
in_file_path = ""
out_file_path = ""
chunk_size = 100_000
citation_thresh = 100
references_thresh = 30
max_fos_per_paper = 5

# Structure of the columns of the paper dataset
col_labels = ("id", "title", "authors", "venue", "year", "n_citation", "page_start", "page_end",
              "doc_type", "publisher", "volume", "issue", "fos", "doi", "references", "abstract")

# Columns and datatypes of the original dataset
dtypes = {"id": "UInt32", "title": "string", "authors": "object", "venue": "object", "year": "UInt16",
          "n_citation": "Uint16", "page_start": "Uint16", "page_end": "Uint16", "doc_type": "string",
          "publisher": "string", "volume": "Uint16", "issue": "Uint16", "fos": "object", "doi": "string",
          "references": "object", "abstract": "object"}


if __name__ == "__main__":
    df = pd.DataFrame()
    is_first_chunk = True

    with pd.read_json(in_file_path, encoding="UTF-8", lines=True, chunksize=chunk_size, dtype=dtypes) as reader:
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

            # Reduce the number of fos per paper
            fos_list = df["fos"].to_numpy()
            for i in range(fos_list.size):
                fos_number = min(len(fos_list[i]), max_fos_per_paper)
                fos_list[i] = [fos_list[i][j] for j in range(fos_number)]

            # Store the paper dataset in a file
            df.to_csv(out_file_path, encoding="UTF-8", mode="a", index=False,
                      header=is_first_chunk, escapechar="|", columns=col_labels)

            is_first_chunk = False

    print("Conversion complete.")
