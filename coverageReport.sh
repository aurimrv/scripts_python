#!/usr/bin/bash

#############################################################################
# This script runs coverage tool on each software product to collect the
# coverage report with respect to line and branch coverage. 
#############################################################################

if (($# < 3))
then
	echo "error: coverageReport.sh <project root dir> <data-file name> <test-set>"
	echo "Example: coverageReport.sh /home/auri/temp/python_experiments2 files.txt 0-ts"
	echo "files.txt must be inside <project root dir>"
	exit
fi

baseDir=$1
dataFile=$2
testSet=$3

projectsData=$(cat "${baseDir}/${dataFile}")

for project in $projectsData
do
	prjArr=($(echo $project | tr ":" "\n"))
	prjDir="${prjArr[0]}"
	clazz="${prjArr[1]}"
	module="${clazz%%.*}"

	echo "Processing program $clazz"
	cd "${baseDir}/${prjDir}"

	echo -e "\tProcessing module ${module}"

	rm -rf "${testSet}/coverage" .coverage .pytest_cache __pycache__ htmlcov

	mkdir "${testSet}/coverage"
	
	coverage run --omit="/home/auri/.pyenv/*,*test_*" --branch -m pytest ./${testSet}/
	coverage report --omit="/home/auri/.pyenv/*,*test_*" > ./${testSet}/coverage/covereageReport.txt
	coverage html --omit="/home/auri/.pyenv/*,*test_*" -d ./${testSet}/coverage
	coverage xml --omit="/home/auri/.pyenv/*,*test_*" -o ./${testSet}/coverage/covereageReport.xml
	coverage json --omit="/home/auri/.pyenv/*,*test_*" -o ./${testSet}/coverage/covereageReport.json
	
	rm -rf .pytest_cache
	rm -rf __pycache__ ./${testSet}/__pycache__
done