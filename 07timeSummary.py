#!/usr/bin/env python3

# Script para a geração da planilha de relatório de tempo de execução das ferramentas.
# Assume-se que existe um arquivo de relatório txt gerado pela ferramenta.

import sys
import os
import re

def main():
    if len(sys.argv) < 4:
        print("error: timeSummary.py <project root dir> <data-file> <test-set-file> <mutation-tool-file>")
        print("Example: timeSummary.py /home/auri/python_experiments2 files.txt test-sets.txt mutation-tools.txt")
        sys.exit(1)

    baseDir = sys.argv[1]
    dataFile = sys.argv[2]
    testSetFile = sys.argv[3]
    mutToolFile = sys.argv[4]
    prjList = baseDir+"/"+dataFile
    testSetList = baseDir+"/"+testSetFile
    mutToolList = baseDir+"/"+mutToolFile

    dadosMutTool = open(mutToolList, 'r')

    for mutTool in dadosMutTool:
        mutTool = mutTool.strip()
        print("Processing mutation tool: ", mutTool)
        dadosTestSets = open(testSetList, 'r')

        for testSet in dadosTestSets:
            testSet = testSet.strip()
            print("Processing test set: ", testSet)
            prjReport = baseDir+"/time-report-"+mutTool+"-"+testSet+".csv"

            dados = open(prjList, 'r')
            output = open(prjReport, 'w')
        
            output.write("project;filename;real;user;sys\n")

            for x in dados:
                x = x.strip()
                info = x.split(':')
                prj = info[0]
                clazz = info[1]
                
                prjDir = baseDir + "/" + prj + "/" + testSet
                
                mutDir = prjDir + "/" + mutTool
                
                isExist = os.path.exists(mutDir)
                if (not isExist):
                    print("Error: project",prj," does not contains cosmic ray data")
                    exit(1)
                    
                processingTimeMetrics(prj, clazz, mutDir, mutTool, output)

            dados.close()
            output.close()
        dadosTestSets.close()
    dadosMutTool.close()

def processingTimeMetrics(prj, clazz, mutDir, mutTool, output):
    reportFile = mutDir + "/" + mutTool + ".time"
    with open(reportFile, 'r') as f:
        for linha in f:
            matchReal = re.search(r'real (\d+\.\d+)', linha)
            if matchReal:
                realTime = float(matchReal.group(1))

            matchUser = re.search(r'user (\d+\.\d+)', linha)
            if matchUser:
                userTime = float(matchUser.group(1))

            matchSys = re.search(r'sys (\d+\.\d+)', linha)
            if matchSys:
                sysTime = float(matchSys.group(1))

        output.write("%s;%s;%.2f;%.2f;%.2f\n" % (prj,clazz,realTime,userTime, sysTime))
        
if __name__ == "__main__":
    main()