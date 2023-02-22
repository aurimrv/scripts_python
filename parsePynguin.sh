#!/usr/bin/bash

if (($# < 5))
then
	echo "error: parsePynguin.py <project root dir> <algorithm1> <algorithm2> <algorithm3> <algorithm4>"
	echo "Example: parsePynguin.py /home/auri/temp/lucca/python_experiments DYNAMOSA MOSA MIO WHOLE_SUITE"
	exit
fi

baseDir=$1
algorithm1=$2
algorithm2=$3
algorithm3=$4
algorithm4=$5

projectsData=$(cat "${baseDir}/files.txt")

tcName="test_pynguin_${algorithm}.py"

for project in $projectsData
do
	prjArr=($(echo $project | tr ":" "\n"))
	prjDir="${prjArr[0]}"
	clazz="${prjArr[1]}"
	module="${clazz%%.*}"

	echo "Processing program $clazz"

	python3 ./pynguin_parser/tc_transformer.py ${baseDir}/${module}/${algorithm1}/test_${module}.py > test_${module}_parsed.py;
    mv test_${module}_parsed.py ${baseDir}/${module}/${algorithm1};
	python3 ./pynguin_parser/tc_transformer.py ${baseDir}/${module}/${algorithm2}/test_${module}.py > test_${module}_parsed.py;
    mv test_${module}_parsed.py ${baseDir}/${module}/${algorithm2};
	python3 ./pynguin_parser/tc_transformer.py ${baseDir}/${module}/${algorithm3}/test_${module}.py > test_${module}_parsed.py;
    mv test_${module}_parsed.py ${baseDir}/${module}/${algorithm3};
	python3 ./pynguin_parser/tc_transformer.py ${baseDir}/${module}/${algorithm4}/test_${module}.py > test_${module}_parsed.py;
    mv test_${module}_parsed.py ${baseDir}/${module}/${algorithm4};
done
