#!/usr/bin/env python3

# Script para a geração da planilha de cobertura de código dos projetos.
# Assume-se que existe um diretório coverage dentro de cada projeto 
# (gerado pelo script coverageReport.sh).

import sys
import os
import xml.dom.minidom

def main():
	if len(sys.argv) < 3:
		print("error: coverageSummary.py <project root dir> <data-file> <test-set>")
		print("Example: coverageSummary.py /home/auri/python_experiments2 files.txt")
		sys.exit(1)

	baseDir = sys.argv[1]
	dataFile = sys.argv[2]
	testSet = sys.argv[3]
	prjList = baseDir+"/"+dataFile
	
	prjReport = baseDir+"/report-coverage-"+testSet+".csv"

	dados = open(prjList, 'r')
	output = open(prjReport, 'w') 

	output.write("project;filename;line coverage;branch coverage\n")

	for x in dados:
		x = x.strip()
		info = x.split(':')
		prj = info[0]
		clazz = info[1]
		
		prjDir = baseDir + "/" + prj + "/" + testSet
		
		coverageDir = prjDir + "/coverage"
		
		isExist = os.path.exists(coverageDir)
		if (not isExist):
			print("Error: project",prj," does not contains coverage data")
			exit(1)
			
		processingCoverageMetrics(prj, clazz, coverageDir, output)

	dados.close()
	output.close()

# Função para processamento dos dados sobre Complexidade
def processingCoverageMetrics(prj, clazz, coverageDir, output):
	doc = xml.dom.minidom.parse(coverageDir+"/covereageReport.xml")
	clazzes = doc.getElementsByTagName("class")
	print("Project", prj, "Class", clazz)
	
	for c in clazzes:
		name = c.getAttribute("filename")
		print("\tProcessing",name)
		if (name == clazz):
			lineCoverage = c.getAttribute("line-rate")
			branchCoverage = c.getAttribute("branch-rate")
			output.write("%s;%s;%.2f;%.2f\n" % (prj,clazz,float(lineCoverage)*100,float(branchCoverage)*100))

if __name__ == "__main__":
    main()