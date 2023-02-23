#!/usr/bin/bash

if (($# < 2))
then
	echo "error: parsePynguin.py <project root dir> <algorithm>"
	echo "Example: parsePynguin.py /home/auri/temp/lucca/python_experiments <DYNAMOSA | MOSA | MIO | WHOLE_SUITE | RANDOM>"
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