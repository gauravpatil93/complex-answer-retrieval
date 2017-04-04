import argparse
from copy import deepcopy
from trec_car.format_runs import *
from tc_ranking import Ranking
from tc_BM25_ranking import BM25
from tc_BM25PLUS_ranking import BM25PLUS
from tc_TFIDF_IMPROVED import TDELTAIDF
from tc_DIRICHLET import DIRICHLET
import cluster_kmeans

parser = argparse.ArgumentParser()
parser.add_argument("outline_file", type=str, help="Qualified location of the outline file")
parser.add_argument("paragraph_file", type=str, help="Qualified location of the paragraph file")
parser.add_argument("output_file", type=str, help="Name of the output file")
args = vars(parser.parse_args())

query_cbor = args['outline_file']
paragraphs_cbor = args['paragraph_file']
output_file_name = args['output_file']

ranking = Ranking(query_cbor, paragraphs_cbor, output_file_name)

query_structure = ranking.gather_queries_and_page()
document_structure = ranking.gather_paragraphs()
docDict = ranking.gather_paragraphs_plain()

bm25_instance = DIRICHLET(query_structure, document_structure, 250)

print("No of queries" + str(len(query_structure)))
print("No of documents" + str(len(document_structure)))

kmeansRankings = []
pageMap = {}
# Generate the query scores
print("Generating the output structure by calculating scores................\n")
query_scores = dict()
queries_parsed = 0
current_page = query_structure[0][3]
pages = [deepcopy(current_page)]
pageQueries = []
pagePassages = []
for query in query_structure:
    if(query[3] != current_page): # new page deal with queries
        pageMap[current_page] = (deepcopy(pageQueries), deepcopy(pagePassages))
        current_page = query[3]
        pages.append(current_page)
        pageQueries = []
        pagePassages = []
        # Need to add

    pageQueries.append(Ranking.process_text_query_plain(query[0]))
    temp_list = []
    tempPassages = []
    print(queries_parsed)
    for key, value in document_structure.items():
        temp_list.append(bm25_instance.document_score(query, key))
        tempPassages.append((docDict[key], key))
    for passage in tempPassages: #limiting number of passages for next step
        if passage not in pagePassages:
            pagePassages.append(passage)

    temp_list.sort(key=lambda m: m[2])
    temp_list.reverse()
    query_scores[query[1]] = deepcopy(temp_list)
    queries_parsed += 1

clusterRankings = []
print()
for key in pageMap.keys():
    clusterRankings.append(cluster_kmeans.runKMeansPipeline((key, pageMap[key][0], pageMap[key][1])))
# Write the results to a file
print("Writing output to file...............................................\n")

#need to format to output a .run file instead
for ranking in clusterRankings:
    print(ranking)
    print("\n")

