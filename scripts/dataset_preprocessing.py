"""
  In this script the whole dataset is cleaned and reduced in size.
  The initial dataset is also split into multiple separate datasets.
  If the script crashes due to memory errors, lower the chunk_size and try again.
"""

import numpy as np
import pandas as pd
import functools
from multiprocessing import Pool

# Config
in_file_path = ""
out_folder_path = ""
chunk_size = 100_000
citation_thresh = 100
references_thresh = 30

# Structure of the columns of the paper of the dataset
col_labels = ("id", "title", "year", "n_citation", "page_start", "page_end", "doc_type",
              "publisher", "volume", "issue", "doi", "references", "abstract")


def author_dataset(dataset, header):
    # Create the author dataset
    author_df = pd.DataFrame(columns=("paper_id", "author_name", "author_id", "author_org"))
    for index, row in dataset[["id", "authors"]].iterrows():
        for author in row["authors"]:
            new_row = {"paper_id": row["id"], "author_name": author.get("name"),
                       "author_id": author.get("id"), "author_org": author.get("org")}
            author_df = pd.concat([author_df, pd.DataFrame([new_row])], ignore_index=True)
    # Store the author dataset in a file
    author_df.to_csv(out_folder_path + "/author_dataset.csv", encoding="UTF-8", mode="a",
                     index=False, header=header, escapechar="|")


def venue_dataset(dataframe, header):
    # Create the venue dataset
    venue_df = pd.DataFrame(columns=("paper_id", "venue_name", "venue_id"))
    for index, row in dataframe[["id", "venue"]].iterrows():
        venue = row["venue"]
        new_row = {"paper_id": row["id"], "venue_name": venue.get("raw"), "venue_id": venue.get("id")}
        venue_df = pd.concat([venue_df, pd.DataFrame([new_row])], ignore_index=True)
    # Store the venue dataset in a file
    venue_df.to_csv(out_folder_path + "/venue_dataset.csv", encoding="UTF-8", mode="a",
                    index=False, header=header, escapechar="|")


def fos_dataset(dataset, header):
    # Create the fos dataset
    fos_df = pd.DataFrame(columns=("paper_id", "fos_name", "fos_weight"))
    for index, row in dataset[["id", "fos"]].iterrows():
        for fos in row["fos"]:
            new_row = {"paper_id": row["id"], "fos_name": fos.get("name"), "fos_weight": fos.get("w")}
            fos_df = pd.concat([fos_df, pd.DataFrame([new_row])], ignore_index=True)
    # Store the venue dataset in a file
    fos_df.to_csv(out_folder_path + "/fos_dataset.csv", encoding="UTF-8", mode="a",
                  index=False, header=header, escapechar="|")


def smap(f):
    return f()


if __name__ == "__main__":
    df = pd.DataFrame()
    is_first_chunk = True

    with pd.read_json(in_file_path, encoding="UTF-8", lines=True, chunksize=chunk_size) as reader:
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

            # Perform the splitting with different threads
            with Pool() as pool:
                pool.map(smap, [functools.partial(author_dataset, df, is_first_chunk),
                                functools.partial(venue_dataset, df, is_first_chunk),
                                functools.partial(fos_dataset, df, is_first_chunk)])

            # Create the paper dataset, by editing the initial one
            df.drop(["authors", "venue", "fos"], axis=1)
            # Store the paper dataset in a file
            df.to_csv(out_folder_path + "/paper_dataset.csv", encoding="UTF-8", mode="a",
                      index=False, header=is_first_chunk, escapechar="|", columns=col_labels)

            is_first_chunk = False

    print("Conversion complete.")
