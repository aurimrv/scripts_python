#!/usr/bin/env python3

# Script que junta todos os dados de tempo em uma única planilha
# Cada coluna do novo arquivo simboliza uma combinação dos algoritmos da pynguin

import sys

def main():
    if len(sys.argv) < 2:
        print("error: coverageCompiled.py <project root dir> <test-sets file name> <type of coverage>")
        print("Example: coverageCompiled.py /home/auri/python_experiments2 test-sets.txt line/branch")
        sys.exit(1)

    baseDir = sys.argv[1]
    testSets = sys.argv[2]
    typeOfCoverage = sys.argv[3]

    prjReport = baseDir+"/compiled-"+typeOfCoverage+"-coverage-report.csv"
    testSetsFileName = baseDir+"/"+testSets

    # cria uma lista vazia para armazenar os dados de cada arquivo
    summaryData = {}

    testSetCount = 1
    with open(testSetsFileName) as testSetsFile:
        for testSet in testSetsFile:
          testSet = testSet.strip()
          reportFileName = baseDir+"/report-coverage-"+testSet+".csv"
          lineCount = 0;
          with open(reportFileName) as reportFile:
            for line in reportFile:
                line = line.strip()
                if (lineCount == 0):
                    lineCount = lineCount + 1
                else:
                    data = line.split(";")
                    if (testSetCount == 1):
                        summaryData[data[0]] = []
                        #summaryData[data[0]].append(data[1])
                    if (typeOfCoverage == 'line'):
                        summaryData[data[0]].append(data[2])
                    elif (typeOfCoverage == 'branch'):
                        summaryData[data[0]].append(data[3])
            testSetCount = testSetCount + 1
    
    with open(prjReport,'w') as outputFile:
        outputFile.write("1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16\n")
        for key in summaryData.keys():
            #outputFile.write(key)
            #outputFile.write(";")
            outputFile.write(';'.join(map(str, summaryData[key])))
            outputFile.write("\n")

if __name__ == "__main__":
    main()