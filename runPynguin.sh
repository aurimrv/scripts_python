#!/usr/bin/bash
#######################################################################
# This script executes pynguin test generator in a set of projects
# to create test set based on an specific supported algorithm:
# DYNAMOSA, MIO, MOSA, WHOLE_SUITE, and RANDOM
#######################################################################
if (($# < 3))
then
	echo "error: runPynguin.sh <project root dir> <algorithm> <seed> [max_timeout(s)]"
	echo "Example: runPynguin.sh /home/auri/temp/lucca/python_experiments DYNAMOSA 1234 5"
	exit
fi

baseDir=$1
algorithm=$2
seed=$3
maxTimeout=600

if (($# >= 4))
then
	maxTimeout=$4
fi

projectsData=$(cat "${baseDir}/files.txt")

for project in $projectsData
do
	prjArr=($(echo $project | tr ":" "\n"))
	prjDir="${prjArr[0]}"
	clazz="${prjArr[1]}"
	module="${clazz%%.*}"

	echo "Processing program $clazz"
	cd "${baseDir}/${module}"

	mkdir ./$algorithm
	
	pynguin --project-path ./ --output-path ./$algorithm --module-name $module -v --create-coverage-report True --algorithm=$algorithm --seed $seed --maximum-search-time $maxTimeout
done
