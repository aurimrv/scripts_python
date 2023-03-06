#!/usr/bin/bash
############################################################################
# This scripts combine two or more different test sets into one directory.
# In this way, both test sets can be evaluated together
############################################################################
if (($# < 3))
then
	echo "error: mergeTestSet.sh <project root dir> <list of test sets directory to be merged>"
	echo "Example: mergeTestSet.sh /home/auri/temp/lucca/python_experiments DYNAMOSA MIO"
	echo "Example: mergeTestSet.sh /home/auri/temp/lucca/python_experiments DYNAMOSA MIO MOSA"
	echo "Example: mergeTestSet.sh /home/auri/temp/lucca/python_experiments DYNAMOSA MIO MOSA WHOLE_SUITE"
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
	
	testSetOutput="${baseDir}/${module}"

	if [ $# -eq 3 ]; then
	   testSetOutput="${testSetOutput}/${2}-${3}"
	elif [ $# -eq 4 ]; then
	   testSetOutput="${testSetOutput}/${2}-${3}-${4}"
	else
	   testSetOutput="${testSetOutput}/${2}-${3}-${4}-${5}"
	fi

	rm -rf $testSetOutput
	mkdir $testSetOutput

	echo -e "\tCopying test sets to $testSetOutput directory"

	for tcDir in $2 $3 $4 $5 $6 $7 $8 $9 
	do
		cp "./${tcDir}/test_${module}_${tcDir}.py" ${testSetOutput}
	done
done