
# MongoDB Queries

- Extract the full text of a document
- Find the publisher who published more articles 


# Creation/update commands

#CREATE A DOCUMENT
db.Project2.insertOne({
	"title" : "Prova1",
       "authors" : [ {
           "name" : "John",
           "id" : "198234",
		"org" : "Org1prova",
		"email" : "io@gmail.com",
		"bio" : "ciao sono una cuoca"
	

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
