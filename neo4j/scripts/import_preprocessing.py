"""
    This script is required to import the paper dataset into Neo4j.
    It modifies the format of the "references" field to make it compatible with the import function.
    The update happens in-place.
"""

import pandas as pd

# Config
file_path = ""

if __name__ == "__main__":
    # Load the dataset
    df = pd.read_csv(file_path, encoding="UTF-8")

    # Adjust the format of the references field
    df['references'] = df['references'].str.replace('[', '')
    df['references'] = df['references'].str.replace(',', ':')
    df['references'] = df['references'].str.replace(' ', '')
    df['references'] = df['references'].str.replace(']', '')

    # Write the updated dataset
    df.to_csv(file_path, encoding="UTF-8", index=False, header=True, escapechar="|")

    print("Operation complete.")
