# coding:utf-8
from numpy import *
import operator
import matplotlib.pyplot as plt

from math import log


def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    lambels = ['A', 'A', 'B', 'B']
    return group, lambels


def classify0(inx, dataset, labels, k):
    datasetsize = dataset.shape[0]
    diffmat = tile(inx, (datasetsize, 1)) - dataset
    sqdiffmat = diffmat ** 2
    sqdistances = sqdiffmat.sum(axis=1)
    distances = sqdistances ** 0.5
    sortedistindicies = distances.argsort()
    classcount = {}
    for i in range(k):
        voteilabel = labels[sortedistindicies[i]]
        classcount[voteilabel] = classcount.get(voteilabel, 0) + 1
    sortedclasscount = sorted(classcount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedclasscount[0][0]


def autonorm(dataset):
    minv = dataset.min(0)
    maxv = dataset.max(0)
    ranges = maxv - minv
    normdataset = zeros(shape(dataset))
    m = dataset.shape(0)
    normdataset = dataset - tile(minv, (m, 1))
    normdataset = normdataset / tile(ranges, (m, 1))
    return normdataset, ranges, minv


def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {},
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries
        shannonEnt -= prob * log(prob, 2) < ---1
    return shannonEnt


decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle='<-')


def loadDataSet():
    postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please1'],
                   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park*', 'stupid'],
                   ['my', 'dalmation', 'is', 'so', 'cute', 'i', 'love', 'him'],
                   ['stop', 'posting', 'stupid1', 'worthless', 'garbage1'],
                   ['me', 'licks', 'ate', 'my', 'steak1', 'how', 'to', 'stop', 'him'],
                   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']
                   ]

    classVec = [0, 1, 0, 1, 0, 1]
    return postingList, classVec


def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)


def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print "the word： %s is not in my Vocabulary! "  % word
    return returnVec


a, b = loadDataSet()
print createVocabList(a)
print setOfWords2Vec(createVocabList(a),a[0])
print setOfWords2Vec(createVocabList(a),a[1])
print setOfWords2Vec(createVocabList(a),a[2])
# group, lambels = createDataSet()
# vc = classify0([1.5, 0], group, lambels, 3)
# print vc
