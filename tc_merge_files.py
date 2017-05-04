"""
Note: This is a static code written only for the purposes of testing 7 million on server
For actual file generation refer to regular parameter taking files like tc_rerank_document_framework.py ( Git readme )
"""

iterator_duo = 0

name_list = []
i = 0
while i != 15:
    name_list.append("partial_files/" + "result_set" + str(i) + ".run")
    i += 1

with open("combined_result_set.run", 'w') as outfile:
    for fname in name_list:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)

