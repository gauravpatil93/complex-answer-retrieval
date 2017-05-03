"""
Note: This is a static code written only for the purposes of testing 7 million on server
For actual file generation refer to regular parameter taking files like tc_rerank_document_framework.py ( Git readme )
"""

import _pickle
import os
from tc_TFIDF_IMPROVED import TDELTAIDF
from copy import deepcopy
from trec_car.format_runs import *
import gc

query_structure = _pickle.load(open(os.path.join(os.curdir, "cache/query_structure_cache_new"), "rb"))

# Generate the query scores
print("Generating the output structure by calculating scores................\n")
query_scores = dict()
queries_parsed = 0
for query in query_structure:
    temp_list = []
    top_n_list = []
    print(queries_parsed)
    document_structure = _pickle.load(open(os.path.join(os.curdir, "merge_cache/para_collection0", "rb")))
    logic_instance = TDELTAIDF(query_structure, document_structure)
    for key, value in document_structure.items():
        temp_list.append(logic_instance.score(query, key))
    document_structure = _pickle.load(open(os.path.join(os.curdir, "merge_cache/para_collection1", "rb")))
    logic_instance = TDELTAIDF(query_structure, document_structure)
    for key, value in document_structure.items():
        temp_list.append(logic_instance.score(query, key))
    document_structure = _pickle.load(open(os.path.join(os.curdir, "merge_cache/para_collection2", "rb")))
    logic_instance = TDELTAIDF(query_structure, document_structure)
    for key, value in document_structure.items():
        temp_list.append(logic_instance.score(query, key))
    document_structure = _pickle.load(open(os.path.join(os.curdir, "merge_cache/para_collection3", "rb")))
    logic_instance = TDELTAIDF(query_structure, document_structure)
    for key, value in document_structure.items():
        temp_list.append(logic_instance.score(query, key))
    document_structure = _pickle.load(open(os.path.join(os.curdir, "merge_cache/para_collection4", "rb")))
    logic_instance = TDELTAIDF(query_structure, document_structure)
    for key, value in document_structure.items():
        temp_list.append(logic_instance.score(query, key))
    document_structure = _pickle.load(open(os.path.join(os.curdir, "merge_cache/para_collection5", "rb")))
    logic_instance = TDELTAIDF(query_structure, document_structure)
    for key, value in document_structure.items():
        temp_list.append(logic_instance.score(query, key))
    document_structure = _pickle.load(open(os.path.join(os.curdir, "merge_cache/para_collection6", "rb")))
    logic_instance = TDELTAIDF(query_structure, document_structure)
    for key, value in document_structure.items():
        temp_list.append(logic_instance.score(query, key))
    document_structure = _pickle.load(open(os.path.join(os.curdir, "merge_cache/para_collection7", "rb")))
    logic_instance = TDELTAIDF(query_structure, document_structure)
    for key, value in document_structure.items():
        temp_list.append(logic_instance.score(query, key))
    document_structure = _pickle.load(open(os.path.join(os.curdir, "merge_cache/para_collection8", "rb")))
    logic_instance = TDELTAIDF(query_structure, document_structure)
    for key, value in document_structure.items():
        temp_list.append(logic_instance.score(query, key))
    document_structure = _pickle.load(open(os.path.join(os.curdir, "merge_cache/para_collection9", "rb")))
    logic_instance = TDELTAIDF(query_structure, document_structure)
    for key, value in document_structure.items():
        temp_list.append(logic_instance.score(query, key))
    document_structure = _pickle.load(open(os.path.join(os.curdir, "merge_cache/para_collection10", "rb")))
    logic_instance = TDELTAIDF(query_structure, document_structure)
    for key, value in document_structure.items():
        temp_list.append(logic_instance.score(query, key))
    document_structure = _pickle.load(open(os.path.join(os.curdir, "merge_cache/para_collection11", "rb")))
    logic_instance = TDELTAIDF(query_structure, document_structure)
    for key, value in document_structure.items():
        temp_list.append(logic_instance.score(query, key))
    document_structure = _pickle.load(open(os.path.join(os.curdir, "merge_cache/para_collection12", "rb")))
    logic_instance = TDELTAIDF(query_structure, document_structure)
    for key, value in document_structure.items():
        temp_list.append(logic_instance.score(query, key))
    document_structure = _pickle.load(open(os.path.join(os.curdir, "merge_cache/para_collection13", "rb")))
    logic_instance = TDELTAIDF(query_structure, document_structure)
    for key, value in document_structure.items():
        temp_list.append(logic_instance.score(query, key))
    document_structure = _pickle.load(open(os.path.join(os.curdir, "merge_cache/para_collection14", "rb")))
    logic_instance = TDELTAIDF(query_structure, document_structure)
    for key, value in document_structure.items():
        temp_list.append(logic_instance.score(query, key))
    document_structure = _pickle.load(open(os.path.join(os.curdir, "merge_cache/para_collection15", "rb")))
    logic_instance = TDELTAIDF(query_structure, document_structure)
    for key, value in document_structure.items():
        temp_list.append(logic_instance.score(query, key))
    document_structure = _pickle.load(open(os.path.join(os.curdir, "merge_cache/para_collection16", "rb")))
    logic_instance = TDELTAIDF(query_structure, document_structure)
    for key, value in document_structure.items():
        temp_list.append(logic_instance.score(query, key))
    document_structure = _pickle.load(open(os.path.join(os.curdir, "merge_cache/para_collection17", "rb")))
    logic_instance = TDELTAIDF(query_structure, document_structure)
    for key, value in document_structure.items():
        temp_list.append(logic_instance.score(query, key))
    document_structure = _pickle.load(open(os.path.join(os.curdir, "merge_cache/para_collection18", "rb")))
    logic_instance = TDELTAIDF(query_structure, document_structure)
    for key, value in document_structure.items():
        temp_list.append(logic_instance.score(query, key))
    document_structure = _pickle.load(open(os.path.join(os.curdir, "merge_cache/para_collection19", "rb")))
    logic_instance = TDELTAIDF(query_structure, document_structure)
    for key, value in document_structure.items():
        temp_list.append(logic_instance.score(query, key))
    document_structure = _pickle.load(open(os.path.join(os.curdir, "merge_cache/para_collection20", "rb")))
    logic_instance = TDELTAIDF(query_structure, document_structure)
    for key, value in document_structure.items():
        temp_list.append(logic_instance.score(query, key))
    document_structure = _pickle.load(open(os.path.join(os.curdir, "merge_cache/para_collection21", "rb")))
    logic_instance = TDELTAIDF(query_structure, document_structure)
    for key, value in document_structure.items():
        temp_list.append(logic_instance.score(query, key))
    document_structure = _pickle.load(open(os.path.join(os.curdir, "merge_cache/para_collection22", "rb")))
    logic_instance = TDELTAIDF(query_structure, document_structure)
    for key, value in document_structure.items():
        temp_list.append(logic_instance.score(query, key))
    document_structure = _pickle.load(open(os.path.join(os.curdir, "merge_cache/para_collection23", "rb")))
    logic_instance = TDELTAIDF(query_structure, document_structure)
    for key, value in document_structure.items():
        temp_list.append(logic_instance.score(query, key))
    document_structure = _pickle.load(open(os.path.join(os.curdir, "merge_cache/para_collection24", "rb")))
    logic_instance = TDELTAIDF(query_structure, document_structure)
    for key, value in document_structure.items():
        temp_list.append(logic_instance.score(query, key))
    document_structure = _pickle.load(open(os.path.join(os.curdir, "merge_cache/para_collection25", "rb")))
    logic_instance = TDELTAIDF(query_structure, document_structure)
    for key, value in document_structure.items():
        temp_list.append(logic_instance.score(query, key))
    temp_list.sort(key=lambda m: m[2])
    temp_list.reverse()
    for elem in temp_list[:1000]:
        top_n_list.append((elem[0][1], elem[1], elem[2]))
    query_scores[query[1]] = deepcopy(top_n_list)
    temp_list.clear()
    top_n_list.clear()
    gc.collect()
    queries_parsed += 1

# Write the results to a file
print("Writing output to file...............................................\n")
with open("new_outline_mod.run", mode='w', encoding='UTF-8') as f:
    writer = f
    temp_list = []
    count = 0
    for k3, value in query_scores.items():
        count += 1
        rank = 0
        for x in value:
            rank += 1
            temp_list.append(RankingEntry(x[0], x[1], rank, x[2]))
    format_run(writer, temp_list, exp_name='test')
    f.close()
