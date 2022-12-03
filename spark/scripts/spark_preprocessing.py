"""
    Thi script prepares the "paper", "venue" and "author datasets to be imported into Spark.
    It adds the ids of the authors and of the venue to the "paper" dataset.
"""

import pandas as pd

# Config
paper_path = ""
venue_path = ""
author_path = ""

if __name__ == "__main__":
    paper = pd.read_csv(paper_path, encoding="UTF-8")
    venue = pd.read_csv(venue_path, encoding="UTF-8")
    author = pd.read_csv(author_path, encoding="UTF-8")

    paper.rename(columns={'id': 'paper_id'}, inplace=True)
    paper = paper.merge(venue, how='left')
    paper.drop(['venue_name'], axis=1, inplace=True)

    venue.drop(['paper_id'], axis=1, inplace=True)
    venue = venue.groupby("venue_id", as_index=False).first()

    id_df = paper['paper_id']
    data = []
    for index, row in id_df.items():
        authors = []
        author_df = author[author["paper_id"] == row]
        for i, r in author_df.iterrows():
            authors.append(r["author_id"])
        data.append([row, authors])
    d = pd.DataFrame(data=data, columns=['paper_id', 'authors'])
    paper = paper.merge(d, how='left')

    author.drop(['paper_id'], axis=1, inplace=True)
    author = author.groupby("author_id", as_index=False).first()

    for index, row in paper.iterrows():
        paper.at[index, 'references'] = str(row['references']).replace('\'', '')

    paper["n_citation"] = paper["n_citation"].astype(int)

    paper.to_csv("paper_spark.csv", encoding="UTF-8", index=False, escapechar="|")
    author.to_csv("author_spark.csv", encoding="UTF-8", index=False, escapechar="|")
    venue.to_csv("venue_spark.csv", encoding="UTF-8", index=False, escapechar="|")
