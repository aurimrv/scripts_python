# Script para a geração da planilha de métricas estáticas
# Demanda que esteja instalada a ferramenta 
# radon (https://pypi.org/project/radon/) do Python 
# para correto funcionamento

import sys
import os
from bs4 import BeautifulSoup as bs
import json

def main():
	if len(sys.argv) < 4:
		print("error: mutationDataCollection.py <project root dir> <algorithm> <seed> [max_timeout(s)]")
		print("Example: python mutationDataCollection.py /home/auri/temp/lucca/python_experiments DYNAMOSA 1234 5")
		sys.exit(1)
	
	baseDir = sys.argv[1]
	algorithm = sys.argv[2]
	seed = sys.argv[3]
	maxTimeout = 600
	if len(sys.argv) >= 5:
		maxTimeout = sys.argv[4]

	prjList = baseDir+"/files.txt"

	dados = open(prjList, 'r')

	# Processing each project
	for x in dados:
		x = x.strip()
		info = x.split(':')
		prj = info[0]
		clazz = info[1]
		module = clazz.removesuffix(".py")
		print(module)

		#Creating default structure
		prjDir = baseDir + "/" + prj
		
		createDir(baseDir, prjDir, "mutmut")
		createDir(baseDir, prjDir, "mutpy")
		createDir(baseDir, prjDir, "mutatest")
		createDir(baseDir, prjDir, "cosmic-ray")
		
		#Executing pynguin test data generator
		cmd = "cd " +  prjDir + ";pynguin --project-path ./ --output-path ./ --module-name " + module + " -v --create-coverage-report True --algorithm="+algorithm+" --seed "+seed+" --maximum-search-time "+ maxTimeout
		print(cmd)
		os.system(cmd)

		exit(0)

		processingCCMetrics(clazz, metricsDir, output)
		processingRawMetrics(clazz, metricsDir, output)
		processingMIMetrics(clazz, metricsDir, output)
		processingHalsteadMetrics(clazz, metricsDir, output)
		
		output.write("\n")

	dados.close()
	output.close()

# Função para processamento dos dados sobre Complexidade
def processingCCMetrics(clazz, metricsDir, output):
	print("Processing CC")
	with open(metricsDir+"/radon-cc.json", 'r') as json_file:
		cc_dict = json.load(json_file)

	#Percorre lista de dicionários procurando por class e methods
	nClazz = 0
	nMethods = 0
	ccMax = 0
	rankCC = 'A'
	for data in cc_dict[clazz]:
		if (data['type'] == 'class'):
			nClazz = nClazz + 1
			nMethods = nMethods + len(data['methods'])
			if (ccMax < data['complexity']):
				ccMax = data['complexity']
			if (rankCC < data['rank']):
				rankCC = data['rank']
	
	output.write("%s;%s;%s;%s;%s" % (clazz,nClazz,nMethods,ccMax,rankCC))

# Função para processamento dos dados sobre Tamanho
def processingRawMetrics(clazz, metricsDir, output):
	print("Processing RAW")
	with open(metricsDir+"/radon-raw.json", 'r') as json_file:
		cc_dict = json.load(json_file)

	#Dados referentes a um módulo python
	data = cc_dict[clazz]
	output.write(";%s;%s" % (data['lloc'],data['sloc']))

# Função para processamento dos dados sobre Maintainability Index
def processingMIMetrics(clazz, metricsDir, output):
	print("Processing MI")
	with open(metricsDir+"/radon-mi.json", 'r') as json_file:
		cc_dict = json.load(json_file)
	
	#Dados referentes a um módulo python
	data = cc_dict[clazz]
	output.write(";%s;%s" % (data['mi'],data['rank']))

# Função para processamento dos dados sobre Maintainability Index
def processingHalsteadMetrics(clazz, metricsDir, output):
	print("Processing Hal")
	with open(metricsDir+"/radon-hal.json", 'r') as json_file:
		cc_dict = json.load(json_file)
		print(cc_dict)

	#Dados referentes a um módulo python
	data = cc_dict[clazz]['total']
	for value in data:
		output.write(";%s" % (value))

def createDir(baseDir, prjDir, nameDir):
		mutDir = prjDir + "/" + nameDir
		
		isExist = os.path.exists(mutDir)
		if (not isExist):
			cmd = "mkdir " + mutDir
			os.system(cmd)

if __name__ == "__main__":
    main()

