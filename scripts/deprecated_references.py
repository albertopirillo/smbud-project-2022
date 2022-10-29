"""
    This script checks if the values in the "references" field of the dataset are valid.
    If a reference points to a paper present in the dataset, it considered valid and kept. Otherwise, it is removed.
    This check is necessary since we are using only a subset of the initial dataset.
    The update happens in-place.
"""

import pandas as pd
from ast import literal_eval

# Config
file_path = ""

if __name__ == "__main__":
    # Load the dataset
    df = pd.read_csv(file_path, encoding="UTF-8")

    # Remove references to non-existing ids
    ref_list_list = df["references"].apply(literal_eval).to_numpy()
    present_ids = set(df["id"])
    df["references"] = [[ref for ref in ref_list if int(ref) in present_ids] for ref_list in ref_list_list]

    # Write the updated dataset
    df.to_csv(file_path, encoding="UTF-8", index=False, header=True, escapechar="|")

    print(f"Operation complete.")
