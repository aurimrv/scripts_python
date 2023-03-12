#!/usr/bin/bash
#####################################################################
# This scripts ensure all test case in a test set runs successfully
# Before executing mutation testing tools, all test set must be
# running successfully.
#####################################################################
if (($# < 1))
then
	echo "error: validateTestSet.sh <project root dir> <data-file name> <test-set data file name>"
	echo "Example: validateTestSet.sh /home/auri/temp/lucca/python_experiments files.txt MIO-MOSA-WHOLE_SUITE"
	echo "You may provide one or directory name with tests"
	exit
fi

baseDir=$1
dataFile=$2
tsDataFile=$3

projectsData=$(cat "${baseDir}/${dataFile}")


# Bulding report header
reportOutput="report-number-of-test-cases.csv"

echo -n "project;filename" > ${baseDir}/${reportOutput}

testSetsData=$(cat "${baseDir}/${tsDataFile}")	
for tcDir in $testSetsData
do
	echo -n ";$tcDir" >> ${baseDir}/${reportOutput}
done
echo "" >> ${baseDir}/${reportOutput}

# Filling report with data

for project in $projectsData
do
	prjArr=($(echo $project | tr ":" "\n"))
	prjDir="${prjArr[0]}"
	clazz="${prjArr[1]}"
	module="${clazz%%.*}"

	cd "${baseDir}/${module}"

	reportOutput="report-number-of-test-cases.csv"

	echo -n "${project};${clazz}" >> ${baseDir}/${reportOutput}

	testSetsData=$(cat "${baseDir}/${tsDataFile}")	
	for tcDir in $testSetsData
	do
		echo "Processing program $clazz - test sets on $tcDir"
		
		testSetOutput="test_${module}_${tcDir}.out"
		python -m pytest ./${tcDir} >& ./${tcDir}/${testSetOutput}
		numberTC=$(awk '{if ($3 == "passed") printf("%d",$2)}' ./${tcDir}/${testSetOutput}) 
		echo -n ";${numberTC}" >> ${baseDir}/${reportOutput}
	done
	echo "" >> ${baseDir}/${reportOutput}

	rm -rf .pytest_cache
	rm -rf __pycache__
	rm -rf ./${tcDir}/__pycache__
done