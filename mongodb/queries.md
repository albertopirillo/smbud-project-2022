
# MongoDB Queries

- Extract the full text of a document
- Find the publisher who published more articles 


# Creation/update commands



# Join operation
```
db.articles.aggregate( [
   {
     $lookup:
       {
         from: "articles",
         localField: "references",
         foreignField: "_id",
         as: "refs"
       }
  }
] )
```