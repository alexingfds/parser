import csv
def ligne(file, sep=","):
    f = open(file, "r")
    r = csv.reader(f, delimiter=sep)
    lignes = list(r)
    f.close()
    print(lignes)
    return lignes
def similarity(lib1,lib2,input):
    arraysource = ligne(input)
    index1 = 0
    index2 = 0
    countapplib1 = 0
    countapplib2 = 0
    similarity = 0

    for elem in arraysource[0]:
        if (elem == lib1):
            index1 = arraysource[0].index(elem)
            # print(index1)
        else:
            if (elem == lib2):
                index2 = arraysource[0].index(elem)
                # print(index2)

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

    print('appuselib1:' + str(countapplib1))
    print('appuselib2:' + str(countapplib2))
    print('similarity apps between lib1 & lib2:' + str(similarity))
    print('amountApp: ' + str(len(arraysource) - 1))
    print('%Usimilarity:' + str(usim))
    print('%average similarity' + str(average_similarity))
    print('moyenne Usimilarity and average_similarity: ' + str((usim + average_similarity) / 2))




if __name__ == "__main__":
    similarity('k','c','samplesortie2.csv')





