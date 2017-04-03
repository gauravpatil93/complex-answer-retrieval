#!/usr/bin/python3

import argparse
import itertools
import numpy
from trec_car.format_runs import *
from trec_car.read_data import *
from pprint import pprint
from copy import deepcopy

parser = argparse.ArgumentParser()
parser.add_argument("toplevel_qrel", type=str, help="Qualified location of top-level qrel")
parser.add_argument("paragraph_file", type=str, help="Qualified location of the paragraph file")
parser.add_argument("output_file", type=str, help="Name of the output file")
parser.add_argument("outline_file", type=str, help = "Name of the outline file")
args = vars(parser.parse_args())

query_cbor = args['outline_file']
qrel_sections = args['toplevel_qrel']
paragraphs_cbor = args['paragraph_file']
output_file_name = args['output_file']

import sklearn.feature_extraction.text as skTextFeatures
import sklearn.pipeline as skPipeline
import sklearn.cluster as skCluster
import sklearn.metrics.pairwise as pairwise
import itertools

def generateTestData():
    pages = []
    with open(query_cbor, 'rb') as f:
        for p in itertools.islice(iter_annotations(f), 0, 1000):
            pages.append(p)

    # Generate queries in plain text
    plain_text_queries = []
    format_to_plaintext = dict()
    map_to_pageName = dict()
    for page in pages:
        for section_path in page.flat_headings_list():
            query_id_plain = " ".join([page.page_name] + [section.heading for section in section_path])
            query_id_formatted = "/".join([page.page_id] + [section.headingId for section in section_path])

            #add map to pageName if needed
            map_to_pageName[query_id_formatted] = page.page_name

            #add map to plaintext if
            format_to_plaintext[query_id_formatted] = query_id_plain
            tup = (page.page_name, query_id_plain, query_id_formatted)
            plain_text_queries.append(tup)

    paragraphs = {}
    with open(paragraphs_cbor, 'rb') as f:
        for p in itertools.islice(iter_paragraphs(f), 0, 1000):
            if (p.para_id not in paragraphs.keys()):
                paragraphs[p.para_id] = str(p)

    outfile = open(str(output_file_name), "w")

    qrels = open(qrel_sections, 'r')
    read_data = qrels.readline()
    pre_data = read_data.split(" ")
    cluster_names = []
    cluster_paragraphs = []

    cluster_pageName = map_to_pageName[pre_data[0]]
    while (read_data != ""):
        read_data = read_data.split(" ")
        try: #some qrel entries are not matched to anything in the source and thus not in format_to_plaintext dictionary
            if(format_to_plaintext[read_data[0]] not in cluster_names):
                cluster_names.append(format_to_plaintext[read_data[0]])
        except:
            read_data = qrels.readline()
            continue
        cluster_paragraphs.append((read_data[2], paragraphs[read_data[2]]))
        read_data = qrels.readline()
        
    return (cluster_pageName, cluster_names, cluster_paragraphs)

def mapToNames(bagsOfWords, section_names):
    maps = {}
    basicMaps = {}
    vectorizer = skTextFeatures.TfidfVectorizer()
    sectionsLength = len(bagsOfWords)

    #Put everything in one bag so we can get cosine similarities
    grabBag = deepcopy(section_names)
    
    for name in bagsOfWords:
        grabBag.append(deepcopy(name))

    grabBagVectors = vectorizer.fit_transform(grabBag)
    similarities = pairwise.cosine_similarity(grabBagVectors)

    availSlots = [0 for b in section_names]
    for name in section_names:
        maps[name] = similarities[section_names.index(name)][len(section_names):]

    permutations = [q for q in itertools.permutations(range(len(section_names)))]
    bestPermutation = range(len(section_names))
    bestScore = 0

    for permutation in permutations:
        score = 0
        for value in permutation:
            section = section_names[permutation.index(value)]
            score += maps[section][value]
        if score > bestScore:
            bestScore = score
            bestPermutation = permutation
    
    for value in bestPermutation:
        section = section_names[bestPermutation.index(value)]
        maps[section] = value

    return maps

def generateRanking(sectionName, bagOfParagraphs, labels):
    ranking = {}
    workList = [sectionName] + bagOfParagraphs
    vectorizer = skTextFeatures.TfidfVectorizer()
    rankingVector = vectorizer.fit_transform(workList)
    similarities = pairwise.cosine_similarity(rankingVector)
    
    #set up hash between labels and scores
    scores = similarities[0][1:]
    for i in range(len(scores)):
        ranking[labels[i]] = scores[i]

    #generate our output list for a ranking
    sortedList = list((ranking.get(i), i) for i in ranking.keys())
    sortedList = sorted(sortedList, key=lambda x: x[0], reverse=True)

    #print out test ranking
    print("SectionName: %s" %(sectionName))
    for i in range(1,len(labels)+1):
        print("%i %s %f" %(i, sortedList[i-1][1],sortedList[i-1][0]))
    print("\n\n")
    return(sortedList)

def runKMeans():
    myData = generateTestData()
    pageName = myData[0]
    cluster_names = myData[1]
    cluster_paragraphs = myData[2] #[0] is id, [1] is text
    cluster_pTexts = [paragraph[1] for paragraph in cluster_paragraphs]

    print("\n\nRunning Kmeans on page ''%s''\n" %(pageName))
    print("Number of clusters %i Number of paragraphs %i\n" %(len(cluster_names), len(cluster_pTexts)))
    vectorizer = skTextFeatures.TfidfVectorizer()
    cluster_vectors = vectorizer.fit_transform(cluster_pTexts)

    km = skCluster.KMeans(n_clusters=len(cluster_names), init='k-means++', max_iter=100, n_init=10)
    km.fit(cluster_vectors)

    finalClusters = [[] for elem in cluster_names]
    finalLabels = [[] for elem in cluster_names]

    for i in range(len(km.labels_)):
        finalClusters[km.labels_[i]].append(deepcopy(cluster_paragraphs[i][1]))
        finalLabels[km.labels_[i]].append(deepcopy(cluster_paragraphs[i][0]))

    bagsOfWords = ["" for elem in cluster_names]
    for i in range(len(cluster_names)):
        for j in finalClusters[i]:
            bagsOfWords[i] += j

    maps = mapToNames(bagsOfWords, cluster_names)
    rankings = []
    for name in cluster_names:
        rankings.append(generateRanking(name,finalClusters[maps[name]],finalLabels[maps[name]]))
    return rankings

def runKMeansPipeline(myData):
    pageName = myData[0]
    cluster_names = myData[1]
    cluster_paragraphs = myData[2] #[0] is id, [1] is text
    cluster_pTexts = [paragraph[1] for paragraph in cluster_paragraphs]

    print("\n\nRunning Kmeans on page ''%s''\n" %(pageName))
    print("Number of clusters %i Number of paragraphs %i\n" %(len(cluster_names), len(cluster_pTexts)))
    vectorizer = skTextFeatures.TfidfVectorizer()
    cluster_vectors = vectorizer.fit_transform(cluster_pTexts)

    km = skCluster.KMeans(n_clusters=len(cluster_names), init='k-means++', max_iter=100, n_init=10)
    km.fit(cluster_vectors)

    finalClusters = [[] for elem in cluster_names]
    finalLabels = [[] for elem in cluster_names]

    for i in range(len(km.labels_)):
        finalClusters[km.labels_[i]].append(deepcopy(cluster_paragraphs[i][1]))
        finalLabels[km.labels_[i]].append(deepcopy(cluster_paragraphs[i][0]))

    bagsOfWords = ["" for elem in cluster_names]
    for i in range(len(cluster_names)):
        #print("Cluster %d\n" % i)
        for j in finalClusters[i]:
            bagsOfWords[i] += j

    maps = mapToNames(bagsOfWords, cluster_names)
    rankings = []
    for name in cluster_names:
        rankings.append(generateRanking(name,finalClusters[maps[name]],finalLabels[maps[name]]))
    #generateRanking(cluster_names[0],finalClusters[maps[cluster_names[0]]],finalLabels[maps[cluster_names[0]]])

    #print(maps[cluster_names[0]])
    #print(maps)
    return rankings


runKMeans()