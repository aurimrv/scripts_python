#!/usr/bin/bash
#######################################################################
# Script that runs Mutatest mutation tool in a set of programs
#######################################################################

if (($# < 2))
then
	echo "error: evalTestOnCosmicRay.sh <project root dir> <test-set-file>"
	echo "Example: evalTestOnCosmicRay.sh /home/auri/temp/lucca/python_experiments test-sets.txt"
	exit
fi

baseDir=$1
testSetFile=$2

tool=mutatest

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

		/usr/bin/time -o ${tool}.time --quiet -p mutatest -s ${module}.py -t "python -m pytest --tb=no ./${tcDir}" -m f -o ${tcDir}/${tool}/${tcDir}-report.rst >& ${tool}.out

		mv ${tool}.time ${tool}.out ./${tcDir}/${tool}

		rm -rf .pytest_cache
		rm -rf __pycache__
		rm -rf ./${tcDir}/__pycache__
	done
done