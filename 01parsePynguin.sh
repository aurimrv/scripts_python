#!/usr/bin/bash
##############################################################################
# This script parses Pynguin generated test sets looking for possible
# problens related to "xfails" annotations.
#############################################################################

if (($# < 2))
then
	echo "error: parsePynguin.sh <project root dir> <algorithm>"
	echo "Example: parsePynguin.sh /home/auri/temp/lucca/python_experiments <DYNAMOSA | MOSA | MIO | WHOLE_SUITE | RANDOM>"
	exit
fi

baseDir=$1
scriptDir=${baseDir}/scripts
algorithm=$2

projectsData=$(cat "${baseDir}/files.txt")

for project in $projectsData
do
	prjArr=($(echo $project | tr ":" "\n"))
	prjDir="${prjArr[0]}"
	clazz="${prjArr[1]}"
	module="${clazz%%.*}"

	echo "Processing program $clazz"

	python3 ${scriptDir}/pynguin_parser/tc_transformer.py ${baseDir}/${module}/${algorithm}/test_${module}.py > test_${module}_${algorithm}.py
	mv ${baseDir}/${module}/${algorithm}/test_${module}.py ${baseDir}/${module}/${algorithm}/test_${module}.py.orig
    mv test_${module}_${algorithm}.py ${baseDir}/${module}/${algorithm}
done