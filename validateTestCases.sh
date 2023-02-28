#!/usr/bin/bash

if (($# < 1))
then
	echo "error: validateTestCases.py <project root dir>"
	echo "Example: validateTestCases.py /home/auri/temp/lucca/python_experiments"
	exit
fi

baseDir=$1

projectsData=$(cat "${baseDir}/files.txt")

for project in $projectsData
do
	prjArr=($(echo $project | tr ":" "\n"))
	prjDir="${prjArr[0]}"
	clazz="${prjArr[1]}"
	module="${clazz%%.*}"

	echo "Processing program $clazz"
	cd "${baseDir}/${module}"

	echo $(pwd)

	for tcDir in "MIO" "MOSA" "WHOLE_SUITE" "DYNAMOSA"
	do
		testSet="test_${module}_${tcDir}.py"
		testSetOutput="test_${module}_${tcDir}.out"

		python -m pytest ./${tcDir}/${testSet} >& ./${tcDir}/${testSetOutput}
	
	    # Only executes if no test errors
		if [ $? -ne 0 ]
		then
			echo "Execution of: python -m pytest ./${tcDir}/${testSet} cause an error"
			echo -e "\tProblem found testing $module - Test Case: $testSet\n"
		fi

		rm -rf .pytest_cache
		rm -rf __pycache__
		rm -rf ./${tcDir}/__pycache__
	done
done