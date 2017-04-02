import argparse
from copy import deepcopy
from trec_car.format_runs import *
from tc_Ranking import Ranking
from tc_BM25_ranking import BM25
from tc_BM25PLUS_ranking import BM25PLUS
from tc_TF_1_DELTA_P_IDF import TDELTAIDF

parser = argparse.ArgumentParser()
parser.add_argument("outline_file", type=str, help="Qualified location of the outline file")
parser.add_argument("paragraph_file", type=str, help="Qualified location of the paragraph file")
parser.add_argument("output_file", type=str, help="Name of the output file")
args = vars(parser.parse_args())

query_cbor = args['outline_file']
paragraphs_cbor = args['paragraph_file']
output_file_name = args['output_file']

ranking = Ranking(query_cbor, paragraphs_cbor, output_file_name)

query_structure = ranking.gather_queries()
document_structure = ranking.gather_paragraphs()

bm25_instance = TDELTAIDF(query_structure, document_structure)

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
        temp_list.append(bm25_instance.t_delta_score(query, key))
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


