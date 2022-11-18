"""
    This script is used to import a dataset in the CSV format into a MongoDB collection.
    It relies on PyMongo, the native Python driver for MongoDB.
"""

from pymongo import MongoClient
import pandas as pd
import ast

# Config
db_address = "mongodb://localhost:27017/"
file_path = r"C:\Users\simon\Desktop\SMBUD-MongoDB\reduced_dataset_author_update.csv"
db_name = "SMBUDProject"
collection_name = "papers_collection"

if __name__ == "__main__":
    with MongoClient(db_address) as client:
        # Connect to the collection and read the dataset
        collection = client[db_name][collection_name]
        df = pd.read_csv(file_path, encoding="UTF-8")

        # Convert string fields to the correct datatype
        df["authors"] = df["authors"].apply(ast.literal_eval)
        df["fos"] = df["fos"].apply(ast.literal_eval)
        df["venue"] = df["venue"].apply(ast.literal_eval)
        df["references"] = df["references"].apply(ast.literal_eval)

        # Insert into the database
        collection.insert_many(df.to_dict('records'))
        print(f"Inserted {len(df)} documents into the database.")
