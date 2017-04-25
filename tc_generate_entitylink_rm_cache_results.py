import _pickle
import argparse
import os
from copy import deepcopy

from trec_car.format_runs import *

from tc_DIRICHLET import DIRICHLET
from tc_Ranking import Ranking
from tc_TFIDF_IMPROVED import TDELTAIDF
from tc_BM25_ranking import BM25
from tc_Rocchio_algo import RocchioAlgorithm
from tc_entitylink_relevance import EntityLinkingAndRelevance

"""
Run this file to generate the results.run file

This file takes 5 arguments.

outline file
paragraph file
output run file
retrieval algorithm (BM25, TFIDFIMPROVED, DIRICHLET)
cache or no_cache

@author: Shilpa Dhagat

"""

parser = argparse.ArgumentParser()
parser.add_argument("outline_file", type=str, help="Qualified location of the outline file")
parser.add_argument("paragraph_file", type=str, help="Qualified location of the paragraph file")
parser.add_argument("output_file", type=str, help="Name of the output file")
parser.add_argument("retrieval_algorithm", type=str, help="BM25, TFIDFIMPROVED, DIRICHLET")
parser.add_argument("use_cache", type=str, help="cache, no_cache")
parser.add_argument("passages_count",type=int, help="no of passages to extract")
args = vars(parser.parse_args())

query_cbor = args['outline_file']
paragraphs_cbor = args['paragraph_file']
output_file_name = args['output_file']
retrieval_algorithm = args['retrieval_algorithm']
cache_flag = args['use_cache']
passages_count = args['passages_count']


def execute_rocchio(query_text, corpus_text, ir):
    print('Executing Rocchio Algorithm')
    # User chooses the value of N (e.g. N=20) first documents in the ranking and marks them as being relevant or non-relevant
    user_input = input(
        "Enter the value of N \n")

    # Convert to a list

    rankings = [list(i) for i in ir.ranking_query[1]]
    pos = 0
    while pos < 20:
        answer = input("Is relevant the document ID " + str(rankings[pos][0]) + " (Y/N)?")
        if (answer == 'y') or (answer == 'Y'):
            rankings[pos][1] = 1
        pos += 1
        # the system updates the original query based on Rocchio's formula.
    rocchio = RocchioAlgorithm(query_text, corpus_text, rankings, ir)

if retrieval_algorithm == 'DIRICHLET':
    if cache_flag == 'cache':
            DIRICHLET.useCache = True
            query_structure = _pickle.load(open(os.path.join(os.curdir, "cache/entitylink/entity_query_structure_cache"), "rb"))
            document_structure = _pickle.load(open(os.path.join(os.curdir, "cache/entitylink/entity_paragraph_structure_cache"), "rb"))
            DIRICHLET.number_of_words_in_the_collection_s = \
                    _pickle.load(open(os.path.join(os.curdir, "cache/entitylink/enhanced_entity_words"), "rb"))
            DIRICHLET.all_words_freq_dict = _pickle.load(open(os.path.join(os.curdir, "cache/entitylink/entity_terms_freq_dict"), "rb"))
            logic_instance = DIRICHLET(query_structure, document_structure, 2500)
    else:
        ranking = Ranking(query_cbor, paragraphs_cbor, passages_count)
        query_structure = ranking.gather_entity_enhanced_queries_mentions()
        document_structure = ranking.gather_entity_enhanced_paragraphs_mentions()
        logic_instance = DIRICHLET(query_structure, document_structure, 2500)

    print("No of queries" + str(len(query_structure)))
    print("No of documents" + str(len(document_structure)))

    # Generate the query scores
    print("Generating the output structure by calculating scores................\n")
    query_scores = dict()
    queries_parsed = 0
    for query in query_structure:
        temp_list = []
        print(queries_parsed)
        for key, value in document_structure.items():
            temp_list.append(logic_instance.score(query, key))
        temp_list.sort(key=lambda m: m[2])
        temp_list.reverse()
        query_scores[query[1]] = deepcopy(temp_list)
        queries_parsed += 1

    # Write the results to a file
    print("Writing output to file...............................................\n")
    with open(output_file_name, mode='w', encoding='UTF-8') as f:
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

elif retrieval_algorithm == 'TFIDFIMPROVED':

    ranking = Ranking(query_cbor, paragraphs_cbor, output_file_name)

    # ranking = EntityLinkingAndRelevance(query_cbor, paragraphs_cbor, output_file_name)

    query_structure = ranking.gather_entity_enhanced_queries_mentions()
    paragraph_structure = ranking.gather_entity_enhanced_paragraphs_mentions()

    # rocchio = execute_rocchio(query_structure, paragraph_structure)

    query_structure = ranking.gather_entity_enhanced_queries_mentions()
    # print(query_structure)
    document_structure = ranking.gather_entity_enhanced_paragraphs_mentions()

    retrival_algo_instance = TDELTAIDF(query_structure, document_structure)

    print("No of queries" + str(len(query_structure)))
    print("No of documents" + str(len(document_structure.keys())))

    # Generate the query scores
    print("Generating the output structure by calculating scores................\n")
    query_scores = dict()
    queries_parsed = 0
    for query in query_structure:
        temp_list = []
        print(queries_parsed)
        for key, value in document_structure.items():
            temp_list.append(retrival_algo_instance.score(query, key))
        temp_list.sort(key=lambda m: m[2])
        temp_list.reverse()
        query_scores[query[1]] = deepcopy(temp_list)
        queries_parsed += 1

    # Write the results to a file
    print("Writing output to file...............................................\n")
    with open(output_file_name, mode='w', encoding='UTF-8') as f:
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

elif retrieval_algorithm == "BM25":

    ranking = Ranking(query_cbor, paragraphs_cbor, output_file_name)

    query_structure = ranking.gather_queries()
    # print(query_structure)
    document_structure = ranking.gather_paragraphs()

    retrival_algo_instance = BM25(query_structure, document_structure)

    print("No of queries" + str(len(query_structure)))
    print("No of documents" + str(len(document_structure.keys())))

    # Generate the query scores
    print("Generating the output structure by calculating scores................\n")
    query_scores = dict()
    queries_parsed = 0
    for query in query_structure:
        temp_list = []
        print(queries_parsed)
        for key, value in document_structure.items():
            temp_list.append(retrival_algo_instance.score(query, key))
        temp_list.sort(key=lambda m: m[2])
        temp_list.reverse()
        query_scores[query[1]] = deepcopy(temp_list)
        queries_parsed += 1

    # Write the results to a file
    print("Writing output to file...............................................\n")
    with open(output_file_name, mode='w', encoding='UTF-8') as f:
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

else:
    exit()


