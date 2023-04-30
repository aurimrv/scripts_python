#!/usr/bin/env python3

# Script para a geração da planilha de relatório de mutantes para a Cosmic Ray.
# Assume-se que existe um arquivo de relatório txt gerado pela ferramenta.

import sys
import os
import sqlite3

def main():
    if len(sys.argv) < 3:
        print("error: cosmicRaySummary.py <project root dir> <data-file> <test-set-file>")
        print("Example: cosmicRaySummary.py /home/auri/temp/lucca/python_experiments files.txt test-sets.txt")
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
        prjReport = baseDir+"/report-cosmic-ray-"+testSet+".csv"

        dados = open(prjList, 'r')
        output = open(prjReport, 'w') 

        output.write("project;filename;mutants;killed_output;killed_timeout;total_killed;survived;mutation score\n")

        for x in dados:
            x = x.strip()
            info = x.split(':')
            prj = info[0]
            clazz = info[1]
        
            prjDir = baseDir + "/" + prj + "/" + testSet

            cosmicRayDir = prjDir + "/cosmic-ray"

            print("Processing data from: ", cosmicRayDir)
        
            isExist = os.path.exists(cosmicRayDir)
            if (not isExist):
                print("Error: project",prj," does not contains cosmic ray data")
                exit(1)
            
            processingCosmicRayMetrics(prj, clazz, cosmicRayDir, output)

        dados.close()
        output.close()
    dadosTestSets.close()

def processingCosmicRayMetrics(prj, clazz, cosmicRayDir, output):
    db_filename = cosmicRayDir + "/"+prj+".sqlite"
    con = sqlite3.connect(db_filename)

    cur = con.cursor()
    # The result of a "cursor.execute" can be iterated over by row
    cur.execute('SELECT count(*) FROM work_results WHERE test_outcome is "SURVIVED";')
    row = cur.fetchone()
    survivingMutants = int(row[0])

    cur.execute('SELECT count(*) FROM work_results WHERE output is not "timeout" and test_outcome is "KILLED";')
    row = cur.fetchone()
    killedByOutputMutants = int(row[0])

    cur.execute('SELECT count(*) FROM work_results WHERE output is "timeout" and test_outcome is "KILLED";')
    row = cur.fetchone()
    killedByTimeoutMutants = int(row[0])

    con.close()

    killedMutants = killedByOutputMutants + killedByTimeoutMutants
    totalMutants = survivingMutants + killedMutants
    mutationScore = (killedMutants/totalMutants)*100

    output.write("%s;%s;%d;%d;%d;%d;%d;%.2f\n" % (prj,clazz,totalMutants,killedByOutputMutants,killedByTimeoutMutants,killedMutants,survivingMutants,mutationScore))

if __name__ == "__main__":
    main()