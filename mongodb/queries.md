
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
	 } ] ,
       "venue" : {
           "raw" : "Information Systems",
           "id" : "121313"
       } ,
	 "year" : 2004,
	 "n_citation" : 123,
	 "page_start" : 345,
	 "page_end" : 409,
	 "doc_type" : "Journal",
	 "publisher" : "New York Times",
	 "volume" : 29,
	 "issue" : 4,
	 "fos" : [ {
           "name" : "Making",
           "w" : 0.343432
	 } ] ,
	 "doi" : "10.2334/301320392",
	 "references" : [ {
           "abstrace" : "Making dedcaisodhasncxiaxzkuc",
           "sections" : "dsscfsxciuky"
	 } ]
})

db.Project2.insertMany([{
	"title" : "Prova1",
       "authors" : [ {
           "name" : "John",
           "id" : "198234",
		"org" : "Org1prova",
		"email" : "io@gmail.com",
		"bio" : "ciao sono una cuoca"
	 } ] ,
       "venue" : {
           "raw" : "Information Systems",
           "id" : "121313"
       } ,
	 "year" : 2004,
	 "n_citation" : 123,
	 "page_start" : 345,
	 "page_end" : 409,
	 "doc_type" : "Journal",
	 "publisher" : "New York Times",
	 "volume" : 29,
	 "issue" : 4,
	 "fos" : [ {
           "name" : "Making",
           "w" : 0.343432
	 } ] ,
	 "doi" : "10.2334/301320392",
	 "references" : [ {
           "abstrace" : "Making dedcaisodhasncxiaxzkuc",
           "sections" : "dsscfsxciuky"
	 } ]
},
{
	"title" : "Prova2",
       "authors" : [ {
           "name" : "Mary",
           "id" : "198234",
		"org" : "Org1prova",
		"email" : "io@gmail.com",
		"bio" : "ciao sono una cuoca"
	 } ] ,
       "venue" : {
           "raw" : "Information Systems",
           "id" : "121313"
       } ,
	 "year" : 2004,
	 "n_citation" : 123,
	 "page_start" : 345,
	 "page_end" : 409,
	 "doc_type" : "Journal",
	 "publisher" : "New York Times",
	 "volume" : 29,
	 "issue" : 4,
	 "fos" : [ {
           "name" : "Making",
           "w" : 0.343432
	 } ] ,
	 "doi" : "10.2334/301320392",
	 "references" : [ {
           "abstrace" : "Making dedcaisodhasncxiaxzkuc",
           "sections" : "dsscfsxciuky"
	 } ]
}
])

#UPDATE A DOCUMENT
db.Project2.updateOne(
   { "id": 101421652, "authors.name": "Cheri Speier"  } ,
   { "$set": { "authors.$.name": "Cheri2" } }
)

#DELETE A DOCUMENT
db.Project2.deleteOne(
   { "id": 104754383 } 
)

#FIND
db.Project2.find(
   { "authors.name": "Cheri Speier"  } 
)

#FIND, PROJECTION AND LIMIT
db.Project2.find(
   { "authors.name": "Cheri2"  },
   {"authors.name":1, "authors.id":1, "authors.org":1, "venue":1} 
)

#LIMIT
db.Project2.find(
   { "year": 2003  },
   {"authors.name":1, "authors.id":1, "authors.org":1, "venue":1} 
).limit(2)

#AND
db.Project2.findOne({
   "$and" : [{"authors.name" : "Cheri2"}, {"year" : 2003}]},
   {"authors.name" : 1, "year" : 1} 
)

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
