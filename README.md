# complex-answer-retrieval (TREC)
Repository contains code submission for CS 980 (Data Science) assignments

```
List of dependencies:

Run on Python 3.5.2
NLTK           :conda install -c anaconda nltk=3.2.2
TREC_CAR_TOOLS :https://github.com/TREMA-UNH/trec-car-tools
RE             :Regular expressions
Stemming       :https://pypi.python.org/pypi/stemming/1.0
_pickle        :Python 3.5 <built_in>
argparse       :conda install -c anaconda argparse=1.3.0
numpy          :conda install -c anaconda numpy=1.12.1 
scipy          :conda install -c anaconda scipy=0.19.0
scikit-learn   :conda install scikit-learn
TagMe          : pip install tagme (GCUBE_TOKEN = "bfbfb535-3683-47c0-bd11-df06d5d96726-843339462")
```
```
Running the code:

The code implements 4 types of ranking functions BM25, BM25+, TFIDF(Delta), DIRICHLET

Caching mechanism implemented for TFIDF(Delta) and DIRICHLET SMOOTHING METHODS so once the cache is generated it can used for both of these methods.

If running tests on TFIDF(Delta) and DIRICHLET
```
# Generating Cache
```
tc_generate_document_cache.py [outlines file] [paragraphs file] [no of passages to extracts from pagagraph file]
```

# Generating trec_eval compatible results file
```
tc_generate_document.py [outlines file] [paragraphs file] [output file] [ranking function] [cache] [no of passages to extract]

The aforementoned arguments can take the following value:

[ranking function]          : BM25, BM25+, TFIDFIMPROVED, DIRICHLET
[cache]                     : no_cache, cache ( Note 'cache' only works if tc_generate_document_cache.py is run first on same number of passages )
[no of passages to extract] : an integer

For first run: The repo already includes a cached collection of 50,000 passages so to test either TFIDF(Delta) or DIRICHLET
just run the following command 

tc_generate_document.py all.test200.cbor.outlines release-v1.4.paragraphs output.DIRICHLET.run DIRICHLET cache 50000
tc_generate_document.py all.test200.cbor.outlines release-v1.4.paragraphs output.DIRICHLET.run TFIDFIMPROVED cache 50000
```


```
Running the code with or without entity linking:

This script runs using main approach with entity linking on test200 data

chmod +x entitylinking.run.sh
./entitylinking.run.sh

This script runs using baseline approach (BM25) on test200 data

chmod +x baseline.run.sh
./baseline.run.sh

```

# NOTE
```
Important note about caching. cPickle has limitations to the amount of data that it can serizalize and store so after running a test on 7 million passages trying to cache them proved that indexes of such a large data set cannot be cached

For the next iteration a pure pythonic full text indexing library can be used such as 
https://pypi.python.org/pypi/Whoosh/
or an alternative to this would be to serialize and store the data in a relational or no-sql database.
```
# Calculating Results

```
eval framework from trec_car 

eval_framework.py [qrels] [run]
```
# Clustering Implementation
```
Implemented by Colin
in folder trec_cluster_basic run the run.sh script to get a sample clustering followed by ranking
Accepts inputs and explains possible input values on running with no arguments.
However, crashes for runs with large sizes of number of clusters (number of queries).


A more efficient method for assigning queries to clusters will be needed for applied use. Almost synced up to run on modified
results for Dirchilets smoothing algorithm but the above problem prevents that.
Not correctly functioning source code for that in trec_cluster_full. For evaluation of how that is coming along the code files not identical to an iteration of Gaurav's implementation are trec_cluster_generate_document.py (the main program file), and cluster_kmeans.py (a callable version of the kmeans clustering and mapping returning rankings). trec_cluster_Ranking.py just has slight modifications to Gaurav's ranking class to have his code give output processable by clustering.
```


# Results 

```
DIRICHLETS SMOOTHING ALGORITHM

using test 200's hierarchichal qrel file and 1,000,000 passages from release1.4.v

map - 0.1423
r-prec - 0.1311

using test 200's hierarchichal qrel file and 4000 passages from training data

map - 0.2782
r-prec - 0.2303

Entity linking performance:

mrr = 0.341,
p@5=0.126,
r-prec=0.191,
map=0.230

Baseline approach

mrr=0.30,
p@5=0.11,
r-prec=0.182,
map=0.223)


```

# Contributions
```
Gaurav Patil: BM25, BM25+, DIRICHLETS, TFIDF Improved, Text Processing Algorithms and Cachcing 
Colin Etzel : Implemented clustering and work towards integrating with DIRICHLETS (see section "Clustering Implementation")
Shilpa Dhagat: Entity linking implementation with Tagme using both annotations and metions(spots) for queries and paragraphs and Greedy interpretation finding algorithm 
```
