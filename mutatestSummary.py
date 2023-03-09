#!/usr/bin/env python3

# Script para a geração da planilha de relatório de mutantes para a Mutates
# Assume-se que existe um arquivo de relatório rst gerado pela ferramenta.

import sys
import os
import re

def main():
    if len(sys.argv) < 3:
        print("error: mutatestSummary.py <project root dir> <data-file> <test-set>")
        print("Example: mutatestSummary.py /home/auri/python_experiments2 files.txt DYNAMOSA")
        sys.exit(1)

    baseDir = sys.argv[1]
    dataFile = sys.argv[2]
    testSet = sys.argv[3]
    prjList = baseDir+"/"+dataFile
    
    prjReport = baseDir+"/report-mutatest-"+testSet+".csv"

    dados = open(prjList, 'r')
    output = open(prjReport, 'w') 

    output.write("project;filename;mutants;killed;survived;mutation score\n")

    for x in dados:
        x = x.strip()
        info = x.split(':')
        prj = info[0]
        clazz = info[1]
        
        prjDir = baseDir + "/" + prj + "/" + testSet
        
        mutatestDir = prjDir + "/mutatest"
        
        isExist = os.path.exists(mutatestDir)
        if (not isExist):
            print("Error: project",prj," does not contains cosmic ray data")
            exit(1)
            
        processingMutatestMetrics(prj, clazz, mutatestDir, testSet, output)

    dados.close()
    output.close()

def processingMutatestMetrics(prj, clazz, mutatestDir, testSet, output):
    reportFile = mutatestDir + "/"+ testSet +"-report.rst"
    with open(reportFile, 'r') as f:
        for linha in f:
            killedMutants = 0
            matchKilled = re.search(r'- DETECTED: (\d+)', linha)
            if matchKilled:
                killedMutants = int(matchKilled.group(1))
            matchTotal = re.search(r'- TOTAL RUNS: (\d+)', linha)
            if matchTotal:
                totalMutants = int(matchTotal.group(1))
        survivingMutants = totalMutants - killedMutants
        mutationScore = (killedMutants/totalMutants)*100
        output.write("%s;%s;%d;%d;%d;%.2f\n" % (prj,clazz,totalMutants,killedMutants, survivingMutants, mutationScore))
        
if __name__ == "__main__":
    main()