#!/usr/bin/python3

import argparse
import numpy
import itertools
from pprint import pprint
from copy import deepcopy

import sklearn.feature_extraction.text as skTextFeatures
import sklearn.pipeline as skPipeline
import sklearn.cluster as skCluster
import sklearn.metrics.pairwise as pairwise

NUM_EXTRA_CLUSTERS = 2

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

    for name in section_names:
        value = numpy.argmax(similarities[section_names.index(name)][len(section_names):])
        print(section_names.index(name))
        print(value)
        maps[name] = value

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
    for i in range(1,len(labels)+1):
        print("%i %s %f" %(i, sortedList[i-1][1],sortedList[i-1][0]))
    print("\n\n")
    return(sortedList)

def runKMeansPipeline(myData):
    pageName = myData[0]
    section_names = myData[1]
    cluster_paragraphs = myData[2] #[0] is id, [1] is text
    cluster_pTexts = [paragraph[1] for paragraph in cluster_paragraphs]
    numClusters = len(section_names) + NUM_EXTRA_CLUSTERS 

    print("\n\nRunning Kmeans on page ''%s''\n" %(pageName))
    print("Number of clusters %i Number of paragraphs %i\n" %(len(numClusters), len(cluster_pTexts)))
    vectorizer = skTextFeatures.TfidfVectorizer()
    cluster_vectors = vectorizer.fit_transform(cluster_pTexts)

    km = skCluster.KMeans(n_clusters=numClusters, init='k-means++', max_iter=100, n_init=10)
    km.fit(cluster_vectors)

    finalClusters = [[] for elem in range(numClusters)]
    finalLabels = [[] for elem in range(numClusters)]

    for i in range(len(km.labels_)):
        finalClusters[km.labels_[i]].append(deepcopy(cluster_paragraphs[i][1]))
        finalLabels[km.labels_[i]].append(deepcopy(cluster_paragraphs[i][0]))

    bagsOfWords = ["" for elem in numClusters]
    for i in range(len(range(numClusters))):
        #print("Cluster %d\n" % i)
        for j in finalClusters[i]:
            bagsOfWords[i] += j

    maps = mapToNames(bagsOfWords, section_names)
    rankings = []
    for name in section_names:
        rankings.append(generateRanking(name,finalClusters[maps[name]],finalLabels[maps[name]]))
    #generateRanking(cluster_names[0],finalClusters[maps[cluster_names[0]]],finalLabels[maps[cluster_names[0]]])

    #print(maps[cluster_names[0]])
    #print(maps)
    return rankings