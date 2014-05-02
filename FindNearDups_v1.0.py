__author__ = 'Arpit'

import sys
from os import listdir
import os
# import pp

SHINGLE_SIZE = 2

def populateShingleMatrix(filelist, path):
    shinglesMatrix = []
    for i in range(len(filelist)):
        with open(path+filelist[i], 'r') as main:
            mainData = main.read()
            shingle = set(get_shingles(mainData, size=SHINGLE_SIZE))
            shinglesMatrix.append(shingle)

    return shinglesMatrix

def findNearDuplicates(filelist, shinglesMatrix, path):
    for i in range(len(shinglesMatrix)-1):
        for j in range(i+1, len(shinglesMatrix)):
            similarity = jaccard(shinglesMatrix[i], shinglesMatrix[j])

            if similarity >= 0.9:
                with open(path + filelist[i], 'r') as main:
                    mainData = main.read()

                with open(path + filelist[i], 'r') as main:
                    childData = main.read()

                if not os.path.exists(path + '/SPAM/'):
                    os.mkdir(path + '/SPAM/')

                if not os.path.exists(path + '/SPAM/' + filelist[i]):
                    writer = open(path + '/SPAM/' + filelist[i], 'w')
                    writer.write(mainData)
                    writer.close()

                if not os.path.exists(path + '/SPAM/' + filelist[j]):
                    writer = open(path + '/SPAM/' + filelist[j], 'w')
                    writer.write(childData)
                    writer.close()

                print 'Similarity: ' + str(similarity) + ' i:' +str(filelist[i]) + ' j:' + str(filelist[j])

def get_shingles(buf, size):
    buf = buf.replace('\n', ' ')
    list = buf.split(' ')

    for i in range(len(list) - size + 1):
        yield tuple(list[i:i+size])

def jaccard(set1, set2):
    x = len(set1.intersection(set2))
    y = len(set1.union(set2))
    return x / float(y)

def populateFileList(path):
    index = 0
    indexList = []

    filelist = listdir(path)

    # Delete the directories from the populated list
    for file in filelist:
        filepath = ''
        filepath = path + file

        if os.path.isdir(filepath):
            indexList.append(index)

        index += 1

    count = 0
    for i in indexList:
        filelist.pop(i-count)
        count += 1

    return filelist

def main():
    path = ''

    argsLength = len(sys.argv)
    if 1 <= len(sys.argv) < 2:
        print 'Please enter command line arguments as below:'
        print 'python tagger.py <Test File>'
        exit()
    if len(sys.argv) == 2:
        path = str(sys.argv[1])
    if len(sys.argv) > 2:
        print 'Please enter exactly one argument to run this script!!!'
        exit()

    if os.path.exists(path):
        if path.rindex('/') != len(path) - 1:
            path = path + '/'
    else:
        print 'Please enter a valid path!!!'
        exit()

    filelist = populateFileList(path)
    shinglesMatrix = populateShingleMatrix(filelist, path)
    findNearDuplicates(filelist, shinglesMatrix, path)

main()