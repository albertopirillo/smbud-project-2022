# System and Methods for Big and Unstructured Data - Project

The aim of the project is to compare different NoSQL database technologies (in particular Neo4j, MongoDB and Apache Spark). 
This was done by implementing a bibliographic database storage solution capable of supporting a large scale data set containing different types of publications ranging from scientific papers, books, articles and so on.

The complete report of the project is available [here](/spark/report/Third%20Delivery%20SMBUD%20-%20Group%2038.pdf)


## Pre-processing
A lot of pre-processing was performed, in order to make the downloaded data sets a good fit for our project.
We have used Python and in particular the [Pandas](https://pandas.pydata.org/) libarry. All the scripts and the notebooks we used are in this repository.

The project report contains detailed instructions on how to use such scripts to generate the exact same data sets that we used and on how to perform the exact same queries we executed.


## Setup
Install all the required Python packages with:

    pip install -r requirements.txt


## First delivery 
The first delivery was about Neo4j, a graph database.
We used a data set downloaded from [AMiner](https://lfs.aminer.cn/misc/dblp.v11.zip). 
After some additional pre-processing, the data set was uploaded into Neo4j and some queries and commands were executed.

The report of this delivery is available [here](/neo4j/report/First%20Delivery%20SMBUD%20-%20Group%2038.pdf)

## Second delivery
The second delivery was about MongoDB, a document-oriented database.
We used the same data set downloaded from [AMiner](https://lfs.aminer.cn/misc/dblp.v11.zip) and some additional data sets to highlight the capabilities of MongoDB at handling sub-documents.  
After some additional pre-processing, the data set was uploaded into MongoDB and some queries and commands were executed.

The report of this delivery is available [here](/mongodb/report/Second%20Delivery%20SMBUD%20-%20Group%2038.pdf)

## Third delivery
The third delivery was about Apache Spark, a framework for large-scale data processing.
We used the same data set downloaded from [AMiner](https://lfs.aminer.cn/misc/dblp.v11.zip).  
After some additional pre-processing, the data set was uploaded into Apache Spark and some queries and commands were executed.

The report of this delivery is available [here](/spark/report/Third%20Delivery%20SMBUD%20-%20Group%2038.pdf)


## Software
- [Draw.io](https://app.diagrams.net/)
- [Neo4j](https://neo4j.com/)
- [MongoDB](https://www.mongodb.com/)
- [Apache Spark](https://spark.apache.org/)
- [Overleaf](https://www.overleaf.com/)
- [Python](https://www.python.org/)
- [PyCharm](https://www.jetbrains.com/pycharm/)
- [Google Colaboratory](https://colab.research.google.com/)

## License
Licensed under [MIT License](LICENSE)
