import csv
import json
from _csv import writer

import numpy

from cluster import Cluster


# def getindex(arraytestsortie):
#     listclustered=[]
#     for elem in arraytestsortie:
#         if(elem[1]!=-1):
#             listclustered.append(arraytestsortie.index(elem) +1)
#     print(listclustered)
#     return listclustered
def getindex(arraytestsortie, nbcluster):
    listclustered = []
    if (nbcluster > 0):
        for i in range(1, nbcluster + 1):
            elemandindex = []
            # print(i)
            for elem in arraytestsortie:

                # i = 1
                if (elem[1] == i):
                    elemandindex.append(arraytestsortie.index(elem) + 1)
            listclustered.append(elemandindex)
        # print(listclustered)
    return (listclustered)


def updateDB(arraysource, index):
    summ = ''
    updict = {}
    tempdict = []
    clusterbyPatern = []

    indextodelete = []
    for cluster in index:
        patternCluster = []
        for point in cluster:
            indextodelete.append(point)
    indextodelete.sort()

    for elem in arraysource:
        ajustindex = 0
        for cluster in index:
            for elemindex in cluster:
                a = elemindex - ajustindex
                # print(ajustindex)
                if (elem[a] != '0' and elem[a] != '1'):
                    summ = summ + elem[a]
                    tempdict.append(dictlibrary.get(elem[a]))
                    # tempdict.insert(0,(dictlibrary.get(elem[a])))
                else:
                    if (elem[a] == '1' and summ != '1'):
                        summ = '1'
                    else:
                        if (summ == ''):
                            summ = '0'

            if (summ != '0' and summ != '1'):
                print(tempdict)
                dictlibrary[summ] = tempdict
                clusterbyPatern.append(tempdict)

                print(dictlibrary)
            elem.append(summ)

            # print(arraysource)
            # print(summ)
            # newcluster.append(summ)
            # print(newcluster)
            # newcluster=[]
            summ = ''
            tempdict = []

        for item in indextodelete:
            thisindex = item - ajustindex
            elem.pop(thisindex)
            ajustindex = ajustindex + 1

    # print(arraysource)
    # print(indextodelete)
    if not (clusterbyPatern == []):
        globalClusterPatern.append(clusterbyPatern)
    return arraysource


def ligne(file, sep=","):
    f = open(file, "r")
    r = csv.reader(f, delimiter=sep)
    lignes = list(r)
    f.close()
    # print(lignes)
    return lignes


def similarity(lib1, lib2, arraysource):
    # arraysource = ligne(input)
    index1 = 0
    index2 = 0
    countapplib1 = 0
    countapplib2 = 0
    similarity = 0

    for elem in arraysource[0]:
        if (elem == lib1):
            index1 = arraysource[0].index(elem)
            # print(index1)
        if (elem == lib2):
            index2 = arraysource[0].index(elem)
        # else:
        #     if (elem == lib2):
        #         index2 = arraysource[0].index(elem)
        #         # print(index2)

    for elem in arraysource:
        if (elem[index1] == elem[index2] and (elem[index1] == '1')):
            similarity = similarity + 1

        if (elem[index1] == '1'):
            countapplib1 = countapplib1 + 1

        if (elem[index2] == '1'):
            countapplib2 = countapplib2 + 1
    lib1similarity = similarity / countapplib1
    lib2similarity = similarity / countapplib2
    usim = similarity / (countapplib2 + countapplib1 - similarity)
    average_similarity = (lib2similarity + lib1similarity) / 2
    return usim


def setlabel(point, data, label):
    for elem in data:
        if (elem[0] == point):
            elem[1] = label


def getlabel(point, data):
    for elem in data:
        if (elem[0] == point):
            return elem[1]


def neigbors(point, data, eps, arraysource):
    neighbors = []
    for elem in data:
        if (elem[0] != point):
            distance = 1 - (similarity(point, elem[0], arraysource))

            if (distance < eps):
                # print(elem[0])
                # elem[1]=1
                neighbors.append(elem[0])
            # print(distance)
    # print(arraypoint)
    # print(neighbors)
    return neighbors


def dbscan(arraysource, minpoint, epsilon):
    arraypoint = []
    C = 0
    # print(arraysource)
    for elem in arraysource[0]:
        if (arraysource[0].index(elem) != 0):
            arraypoint.append([elem, 0])

    # print(arraypoint)
    # print(len(arraypoint))
    for elem in arraypoint:

        # print(elem[0]+' est visite ================================================')
        if (elem[1] == 0):
            npoints = neigbors(elem[0], arraypoint, epsilon, arraysource)
            # print(elem[0] + ' est visite ***************'+ str(npoints)+'==='+ str(len(npoints))+ ' de voisin')

            if (len(npoints) < minpoint):
                elem[1] = -1

            else:
                C += 1
                i = 0
                elem[1] = C
                # fix code for elem
                while i < len(npoints):
                    pn = npoints[i]
                    thislabelph = getlabel(pn, arraypoint)
                    if (thislabelph == -1):
                        setlabel(pn, arraypoint, C)

                    elif (thislabelph == 0):
                        setlabel(pn, arraypoint, C)
                        # print(arraypoint)

                        pnneighborpts = neigbors(pn, arraypoint, epsilon, arraysource)
                        if (len(pnneighborpts) >= minpoint):
                            npoints = npoints + pnneighborpts
                    i += 1
    print(arraypoint)
    output = Cluster(arraypoint, C, C)
    return output


def relaxdbscan(arraysource, epsilon, minpoint):
    history = []
    pas = 0.1
    while (epsilon <= 1):
        resultdbscan = dbscan(arraysource, minpoint, epsilon)
        history.append(resultdbscan.getarray())
        indextoremove = getindex(resultdbscan.getarray(), resultdbscan.getnbcluste())
        # print('cluster' + str(resultdbscan.getnbcluste()))
        print('element to remove' + str(indextoremove))
        arraysource = updateDB(arraysource, indextoremove)
        # print(arraysource)
        epsilon = epsilon + pas
        print('epsilon = ' + str(epsilon))
    # print(history)
    return resultdbscan.getarray()

    # while (epsilonn <1):
    #     relaxdbscan(arraysource,epsilonn,minpoint)


###### visualisationn#############


def child(name, value):
    temp = {"name": name, "value": value}
    return temp

    data["children"].append(temp)


# fonction flat array
def getAllClusters(resultdbscan, dictlibrary):
    # reslutdbscan=[['f', -1], ['azde', -1], ['cmnukbgj', -1]]
    tempArrayofClusters = []

    ArrayofClusters = []
    for elem in resultdbscan:
        dataelem = dictlibrary.get(elem[0])
        if (isinstance(dataelem, list)):
            if (dataelem not in ArrayofClusters):
                ArrayofClusters.append(dataelem)
        else:
            tempArrayofClusters.append(dataelem)
        ### elenver les element qui ne sont pas clustered
        # ArrayofClusters.append(tempArrayofClusters)
        tempArrayofClusters = []
    # print("arrayofclusters")
    # print(ArrayofClusters)
    return ArrayofClusters


def souscluster(clusters):
    tempdataa = []

    # clusters = ['c', 'm', 'n', 'u', ['k', 'b', ['g', 'j']]]
    for elem in clusters:
        if not (isinstance(elem, list)):
            tempdataa.append(elem)
            # return data

        else:
            # dataa.append(tempdataa)
            tempelem = elem
            # print(elem)
            souscluster(tempelem)
        # print(tempdataa)
        if (tempdataa not in dataa):
            dataa.append(tempdataa)
    return dataa


def hiearchyCluster(childcluster):
    temp = 0
    for elem in childcluster:
        # print(elem)
        if (temp == 0):
            temp = elem
            # print(temp)
        else:
            # print("yes")
            # print(elem["children"])
            elem["children"].append(temp)
            temp = elem
            # print(temp)

    return temp


def superCluster(hiarchyCluster):
    data = {"name": "Library", "children": []}
    data['children'].append(hiarchyCluster)
    return data


def subchildtwo(cluster):
    dataarray = []
    for array in cluster:
        data = {"name": "Library", "children": []}
        for elem in array:
            data['children'].append(child(elem, 4888))
        dataarray.append(data)
    # print(dataarray)
    # print(len(dataarray))
    # reverse array
    return dataarray[::-1]


def geteachCluster(resultgetallclusters):
    for elem in resultgetallclusters:
        subdatajson.append(superCluster(hiearchyCluster(subchildtwo(souscluster(elem)))))
        # print("etat de data")
        # print(dataa)
        dataa.clear()
    return subdatajson


def globaljsonvisualisation(subdatajson):
    data = {"name": "Library", "children": []}
    for elem in subdatajson:
        data['children'].append(elem)
    return data
# ############################# Puc#####################
def flatten(S):
    if S == []:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]) + flatten(S[1:])
    return S[:1] + flatten(S[1:])

def puc(pattern):
    # result = ['a', 'z', 'd', 'y']
    result = flatten(pattern)
    print(result)
    listofIndex = []
    NbrUseLibByApp = []
    NotnullAppUseLib = 0
    for elem in arraysource[0]:
        if (elem in result):
            index = arraysource[0].index(elem)
            listofIndex.append(index)

    for element in arraysource:
        if not(arraysource.index(element) == 0):
            NbrappUseLib = 0
            for indexlib in listofIndex:
                if(element[indexlib] =='1'):
                    NbrappUseLib =NbrappUseLib+1
            NbrUseLibByApp.append(NbrappUseLib)
            if not (NbrappUseLib ==0):
                NotnullAppUseLib = NotnullAppUseLib +1
        print(NbrUseLibByApp)
        print(NotnullAppUseLib)
    Sum = sum(NbrUseLibByApp)
    print(Sum)
    numerateur =Sum/len(result)
    PUC =numerateur/NotnullAppUseLib
    print('PUC==> ' + str(PUC))
    return PUC
def averagePuc(listofpattern):
    SumPuc=0
    for elem in listofpattern:
        SumPuc = SumPuc+puc(elem)

    AveragePuc =SumPuc/(len(listofpattern))
    print('AveragePuc==> ' + str(AveragePuc))
    return AveragePuc

def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)
if __name__ == "__main__":
    print('My DBSC')
    globalClusterPatern = []
    # C = 0
    # index = [1, 2, 3]
    dataa = []
    subdatajson = []
    resultdbscan =[['f', -1], ['cmnu', -1], ['ejqazdykbgpi', -1]]

    minpt = 3
    eps = 0.1

    dictlibrary = {}
    file = 'samplesortie2.csv'

    arraysource = ligne(file)
    arraysourc = ligne(file)

    for elem in arraysourc[0]:
        if (arraysourc[0].index(elem) != 0):
            dictlibrary[str(elem)] = elem
    # print(dictlibrary)
    print('nombre de librairies: ' + str(len(arraysourc[0])))
    print('nombre dapplications :' + str(len(arraysourc)))
    reslutdbscan = relaxdbscan(arraysourc, eps, minpt)
    print("gobal patern")
    print(len(globalClusterPatern))
    print(globalClusterPatern)
    averagePuc(globalClusterPatern[len(globalClusterPatern)-1])
    # puc(['a', 'z', 'd', 'y'])
    # print(arraysource)

    print(globalClusterPatern[len(globalClusterPatern)-1])
    with open('data.json', 'w') as fp:
        json.dump(globaljsonvisualisation(geteachCluster(getAllClusters(reslutdbscan, dictlibrary))), fp, indent=4)



























