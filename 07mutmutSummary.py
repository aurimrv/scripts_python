#!/usr/bin/env python3

# Script para a geração da planilha de relatório de mutantes para a MutMut.
# Assume-se que existe um arquivo de relatório html gerado pela ferramenta.

import sys
import os
import re

def main():
    if len(sys.argv) < 3:
        print("error: mutmutSummary.py <project root dir> <data-file> <test-set-file>")
        print("Example: mutmutSummary.py /home/auri/python_experiments2 files.txt test-sets.txt")
        sys.exit(1)

    baseDir = sys.argv[1]
    dataFile = sys.argv[2]
    testSetFile = sys.argv[3]
    prjList = baseDir+"/"+dataFile
    testSetList = baseDir+"/"+testSetFile

    dadosTestSets = open(testSetList, 'r')

    for testSet in dadosTestSets:
        testSet = testSet.strip()
        print("Processing test set: ", testSet)
        prjReport = baseDir+"/report-mutmut-"+testSet+".csv"

        dados = open(prjList, 'r')
        output = open(prjReport, 'w')  

        output.write("project;filename;mutants;killed;survived;mutation score\n")

        for x in dados:
            x = x.strip()
            info = x.split(':')
            prj = info[0]
            clazz = info[1]
            
            prjDir = baseDir + "/" + prj + "/" + testSet
            
            mutmutDir = prjDir + "/mutmut"
            
            isExist = os.path.exists(mutmutDir)
            if (not isExist):
                print("Error: project",prj," does not contains mutpy data")
                exit(1)
                
            processingMutMutMetrics(prj, clazz, mutmutDir, output)

        dados.close()
        output.close()
    dadosTestSets.close()

def processingMutMutMetrics(prj, clazz, mutpyDir, output):
    reportFile = mutpyDir + "/mutmut.out"

    with open(reportFile, 'r') as f:
        last_line = f.readlines()[-1]
    last_line = last_line.strip()

    values = last_line.split()
    
    totalMutants = int(values[1].split("/")[1])
    killedMutants = int(values[3])
    timeoutMutants = int(values[5])
    suspiciousMutants = int(values[7])
    survivingMutants = int(values[9])
    skippedMutants = int(values[11])

    killedMutants = killedMutants + timeoutMutants + suspiciousMutants
    totalMutants = totalMutants - skippedMutants

    mutationScore = (killedMutants/totalMutants)*100
    output.write("%s;%s;%d;%d;%d;%.2f\n" % (prj,clazz,totalMutants,killedMutants, survivingMutants, mutationScore))

def read_n_to_last_line(filename, n = 1):
    """Returns the nth before last line of a file (n=1 gives last line)"""
    num_newlines = 0
    with open(filename, 'rb') as f:
        try:
            f.seek(-2, os.SEEK_END)    
            while num_newlines < n:
                f.seek(-2, os.SEEK_CUR)
                if f.read(1) == b'\n':
                    num_newlines += 1
        except OSError:
            f.seek(0)
        last_line = f.readline().decode()
    return last_line

def processingMutMutMetricsFromHTML(prj, clazz, mutpyDir, output):
    reportFile = mutpyDir + "/html/index.html"
    with open(reportFile, 'r') as f:
        for linha in f:
            matchKilled = re.search(r'Killed (\d+)', linha)
            if matchKilled:
                killedMutants = int(matchKilled.group(1))

            matchTotal = re.search(r'out of (\d+)', linha)
            if matchTotal:
                totalMutants = int(matchTotal.group(1))

        survivingMutants = totalMutants - killedMutants  
        mutationScore = (killedMutants/totalMutants)*100
        output.write("%s;%s;%d;%d;%d;%.2f\n" % (prj,clazz,totalMutants,killedMutants, survivingMutants, mutationScore))
        
if __name__ == "__main__":
    main()