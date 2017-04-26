iterator_duo = 0

name_list = []
i = 0
while i != 10:
    name_list.append("partial_files/" + "result_set" + str(i) + ".run")
    i += 1

with open("combined_result_set.run", 'w') as outfile:
    for fname in name_list:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)

