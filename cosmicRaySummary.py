#!/usr/bin/env python3

# Script para a geração da planilha de relatório de mutantes para a Cosmic Ray.
# Assume-se que existe um arquivo de relatório txt gerado pela ferramenta.

import sys
import os
import re

def main():
    if len(sys.argv) < 3:
        print("error: cosmicRaySummary.py <project root dir> <data-file> <test-set>")
        print("Example: cosmicRaySummary.py /home/auri/python_experiments2 files.txt DYNAMOSA")
        sys.exit(1)

    baseDir = sys.argv[1]
    dataFile = sys.argv[2]
    testSet = sys.argv[3]
    prjList = baseDir+"/"+dataFile
    
    prjReport = baseDir+"/report-cosmic-ray-"+testSet+".csv"

    dados = open(prjList, 'r')
    output = open(prjReport, 'w') 

    output.write("project;filename;mutants;killed;survived;mutation score\n")

    for x in dados:
        x = x.strip()
        info = x.split(':')
        prj = info[0]
        clazz = info[1]
        
        prjDir = baseDir + "/" + prj + "/" + testSet
        
        cosmicRayDir = prjDir + "/cosmic-ray"
        
        isExist = os.path.exists(cosmicRayDir)
        if (not isExist):
            print("Error: project",prj," does not contains cosmic ray data")
            exit(1)
            
        processingCosmicRayMetrics(prj, clazz, cosmicRayDir, output)

    dados.close()
    output.close()


def processingCosmicRayMetrics(prj, clazz, cosmicRayDir, output):
    reportFile = cosmicRayDir + "/report_cosmicray.txt"
    with open(reportFile, 'r') as f:
        for linha in f:
            matchTotal = re.search(r'complete: (\d+)', linha)
            if matchTotal:
                totalMutants = int(matchTotal.group(1))
            matchSurviving = re.search(r'surviving mutants: (\d+)', linha)
            if matchSurviving:
                survivingMutants = int(matchSurviving.group(1))
        killedMutants = totalMutants - survivingMutants
        mutationScore = (killedMutants/totalMutants)*100
        output.write("%s;%s;%d;%d;%d;%.2f\n" % (prj,clazz,totalMutants,killedMutants, survivingMutants, mutationScore))
        
if __name__ == "__main__":
    main()