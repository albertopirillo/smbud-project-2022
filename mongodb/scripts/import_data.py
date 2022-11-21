"""
    This script is used to import a dataset in the CSV format into a MongoDB collection.
    It relies on PyMongo, the native Python driver for MongoDB.
"""

from pymongo import MongoClient
from bson.objectid import ObjectId
import pandas as pd
import ast

# Config
db_address = "mongodb://localhost:27017/"
file_path = ""
db_name = ""
collection_name = ""

if __name__ == "__main__":
    with MongoClient(db_address) as client:
        # Connect to the collection and read the dataset
        collection = client[db_name][collection_name]
        df = pd.read_csv(file_path, encoding="UTF-8")

        # Convert string fields to the correct datatype
        df["authors"] = df["authors"].apply(ast.literal_eval)
        df["fos"] = df["fos"].apply(ast.literal_eval)
        df["venue"] = df["venue"].apply(ast.literal_eval)

        # Convert references to ObjectId
        df["references"] = df["references"].apply(ast.literal_eval)
        allReferencesFromDF = df["references"]
        allReferencesNew = []
        for refList in allReferencesFromDF:
            tempRefList = []
            for ref in refList:
                additionalChars = ""
                for k in range(0, 24 - len(str(ref))):
                    additionalChars = additionalChars + "0"
                new_ref = str(ref) + additionalChars
                tempRefList.append(ObjectId(new_ref))
            allReferencesNew.append(tempRefList)
        df["references"] = allReferencesNew

        # Convert sections to the correct datatype
        df["sections"] = df["sections"].apply(ast.literal_eval)

        # Convert the "id" field into an ObjectId and change its name
        allIdsFromDF = df["id"].astype(str)
        allIdsNew = []
        for eachId in allIdsFromDF:
            additionalChars = ""
            for k in range(0, 24-len(str(eachId))):
                additionalChars = additionalChars + "0"
            newIdString = str(eachId) + additionalChars
            allIdsNew.append(ObjectId(newIdString))

        df["id"] = allIdsNew
        df = df.rename({"id": "_id"}, axis=1)

        # Insert into the database
        collection.insert_many(df.to_dict('records'))
        print(f"Inserted {len(df)} documents into the database.")
