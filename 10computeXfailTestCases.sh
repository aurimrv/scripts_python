#!/usr/bin/bash
#####################################################################
# This scripts ensure all test case in a test set runs successfully
# Before executing mutation testing tools, all test set must be
# running successfully.
#####################################################################
if (($# < 1))
then
	echo "error: validateTestSet.sh <project root dir> <algoritms>"
	echo "Example: 10computeXfailTestCases.sh /home/auri/temp/lucca/python_experiments MIO MOSA WHOLE_SUITE DYNAMOSA RANDOM"
	echo "You may provide one or more algorithms names"
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

	#echo "Processing program $clazz"
	cd "${baseDir}/${module}"

	#echo $(pwd)

	echo -n "$module"

	for tcDir in $2 $3 $4 $5 $6 $7 $8 $9 
	do
		originalTestSet="${tcDir}/test_${module}.py.orig"
		
		xfail=$(grep "xfail" $originalTestSet | wc -l)
		total=$(grep "test_case" $originalTestSet | wc -l)

		echo -n ";$tcDir;$xfail;$total"
	done
	echo ""
done