#!/usr/bin/bash

if (($# < 6))
then
	echo "error: runPynguin.py <project root dir> <algorithm1> <algorithm2> <algorithm3> <algorithm4> <seed> [max_timeout(s)]"
	echo "Example: runPynguin.py /home/auri/temp/lucca/python_experiments DYNAMOSA 1234 5"
	exit
fi

baseDir=$1
algorithm1=$2
algorithm2=$3
algorithm3=$4
algorithm4=$5
seed=$6
maxTimeout=600

if (($# >= 7))
then
	maxTimeout=$7
fi

projectsData=$(cat "${baseDir}/files.txt")

tcName="test_pynguin_${algorithm}.py"

for project in $projectsData
do
	prjArr=($(echo $project | tr ":" "\n"))
	prjDir="${prjArr[0]}"
	clazz="${prjArr[1]}"
	module="${clazz%%.*}"

	echo "Processing program $clazz"
	cd "${baseDir}/${module}"

	pynguin --project-path ./ --output-path ./$algorithm1 --module-name $module -v --create-coverage-report True --algorithm=$algorithm1 --seed $seed --maximum-search-time $maxTimeout;
    pynguin --project-path ./ --output-path ./$algorithm2 --module-name $module -v --create-coverage-report True --algorithm=$algorithm2 --seed $seed --maximum-search-time $maxTimeout;
    pynguin --project-path ./ --output-path ./$algorithm3 --module-name $module -v --create-coverage-report True --algorithm=$algorithm3 --seed $seed --maximum-search-time $maxTimeout;
    pynguin --project-path ./ --output-path ./$algorithm4 --module-name $module -v --create-coverage-report True --algorithm=$algorithm4 --seed $seed --maximum-search-time $maxTimeout;
done
