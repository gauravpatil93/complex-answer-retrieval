import _pickle
import argparse
import os

from tc_Ranking import Ranking

"""
Before using the cache based implementation run this file this creates the cache required to speed up things
in the ranking functions.

The caches are stored in the ./cache directory.

@author Gaurav Patil
"""

parser = argparse.ArgumentParser()
parser.add_argument("outline_file", type=str, help="Qualified location of the outline file")
parser.add_argument("paragraph_file", type=str, help="Qualified location of the paragraph file")
args = vars(parser.parse_args())

query_cbor = args['outline_file']
paragraphs_cbor = args['paragraph_file']


ranking = Ranking(query_cbor, paragraphs_cbor, enable_cache=True)

query_structure = ranking.gather_queries()
document_structure = ranking.gather_paragraphs()

# Build cache for no of documents containing a specific word:
no_of_docs_with_term = dict()
for elem in query_structure:
    for key, value in elem[2].items():
        for k, v in document_structure.items():
            if key in v:
                if key in no_of_docs_with_term:
                    no_of_docs_with_term[key] += 1
                else:
                    no_of_docs_with_term[key] = 1
_pickle.dump(no_of_docs_with_term, open(os.path.join(os.curdir, "_cache/no_of_docs_with_term"), "wb"))


# Build cache for average document length
summ = 0
for para_id, ranked_words_dict in document_structure.items():
    summ += sum(ranked_words_dict.values())
average = summ / float(len(document_structure))
_pickle.dump(average, open(os.path.join(os.curdir, "_cache/average_length_of_documents"), "wb"))


# Build cache for DIRICHLET
# Total no of words in the collection
for elem in query_structure:
    summ += sum(elem[2].values())
_pickle.dump(summ, open(os.path.join(os.curdir, "_cache/no_of_words_in_the_collection"), "wb"))

# Frequency of all terms in the dictionary
all_terms_frequency_dict = dict()

for kkk, vvv in document_structure.items():
    for kkkk, vvvv in vvv.items():
        if kkkk in all_terms_frequency_dict:
            all_terms_frequency_dict[kkkk] += vvvv
        else:
            all_terms_frequency_dict[kkkk] = vvvv
for ele in query_structure:
    for kkkkk, vvvvv in ele[2].items():
        if kkkkk in all_terms_frequency_dict:
            all_terms_frequency_dict[kkkkk] += vvvvv
        else:
            all_terms_frequency_dict[kkkkk] = vvvvv
_pickle.dump(all_terms_frequency_dict, open(os.path.join(os.curdir, "_cache/all_terms_freq_dict"), "wb"))


