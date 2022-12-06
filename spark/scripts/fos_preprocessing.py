"""
    This script is used to reshape the fos and paper datasets.
    The fos are grouped by name and their average weight is computed.
    Then a unique id is generated and the "paper_id" field is dropped.
    For each paper, we add the id of the fos that it covers.
"""

import pandas as pd

# Config
fos_path = ""
paper_path = ""

if __name__ == "__main__":
    df = pd.read_csv(fos_path, encoding="UTF-8")
    paper_df = pd.read_csv(paper_path, encoding="UTF-8")

    # Group the fos by name and compute the average of the weights
    fos_df = df.groupby("fos_name")["fos_weight"].mean().reset_index()

    # Generate a unique *id* and add it to the Dataframe:
    fos_id = [100000 + i for i in range(len(fos_df))]
    fos_df["id"] = fos_id

    # Merge together the paper_id with the new fos ids
    old_fos_df = pd.read_csv(fos_path, encoding="UTF-8")
    old_df = pd.merge(old_fos_df[["paper_id", "fos_name"]], fos_df, on="fos_name")

    # Group in a single row all fos that a paper covers
    old_df = old_df.groupby("paper_id")["id"].apply(list).reset_index()
    old_df = old_df.rename({"id": "fos_id"}, axis=1)

    # Add such fos_ids to the paper dataset:
    paper_df = pd.merge(paper_df, old_df, how="left", on="paper_id")

    # Store the two datasets
    fos_df = fos_df.rename({"fos_weight": "weight", "fos_name": "name"}, axis=1)
    fos_df = fos_df[["id", "name", "weight"]]
    fos_df.to_csv("fos_spark.csv", encoding="UTF-8", index=False, escapechar="|")
    paper_df.to_csv("paper_spark.csv", encoding="UTF-8", index=False, escapechar="|")
