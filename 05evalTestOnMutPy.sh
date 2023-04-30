#!/usr/bin/bash
#######################################################################
# Script that runs Mut.Py mutation tool in a set of programs
#######################################################################

if (($# < 2))
then
	echo "error: evalTestOnCosmicRay.sh <project root dir> <test-set-file>"
	echo "Example: evalTestOnCosmicRay.sh /home/auri/temp/lucca/python_experiments test-sets.txt"
	exit
fi

baseDir=$1
testSetFile=$2

tool=mutpy

# Iterando sobre o arquivo de test-sets
testSetData=$(cat "${baseDir}/${testSetFile}")
for testSet in $testSetData
do

	projectsData=$(cat "${baseDir}/files.txt")

	for project in $projectsData
	do
		prjArr=($(echo $project | tr ":" "\n"))
		prjDir="${prjArr[0]}"
		clazz="${prjArr[1]}"
		module="${clazz%%.*}"

		echo "Processing program $clazz"
		cd "${baseDir}/${module}"

		# Cleaning previous report
		rm -rf ./${tcDir}/${tool}
		mkdir ./${tcDir}/${tool}

		cmd="mut.py -e -m -c --debug -t ${module}.py -u ./${tcDir} --runner pytest --tb=no --report-html ./${tcDir}/${tool}"

		/usr/bin/time -o ${tool}.time --quiet -p $cmd >& ${tool}.out

		mv ${tool}.time ${tool}.out ./${tcDir}/${tool}

		rm -rf __pycache__
		rm -rf ./${tcDir}/__pycache__
	done
done