# complex-answer-retrieval (TREC)
Repository contains code submission for CS 980 (Data Science) assignments

```
List of dependencies:

NLTK           :conda install -c anaconda nltk=3.2.2
TREC_CAR_TOOLS :https://github.com/TREMA-UNH/trec-car-tools
RE             :Regular expressions
Stemming       :https://pypi.python.org/pypi/stemming/1.0
_pickle        :Python 3.5 <built_in>
argparse       :conda install -c anaconda argparse=1.3.0
numpy          :conda install -c anaconda numpy=1.12.1 
scipy          :conda install -c anaconda scipy=0.19.0
scikit-learn   :conda install scikit-learn
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

Following are the links to download the already generated files using the above steps:


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
# sample clustering implementation
  in folder trec_cluster_basic run the run.sh script 
  
# Results 


