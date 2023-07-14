#!/usr/bin/bash
#######################################################################
# Script that runs Mutatest mutation tool in a set of programs
#######################################################################

if (($# < 3))
then
	echo "error: 05evalTestOnCosmicRay.sh <project root dir> <data-file> <test-set-file>"
	echo "Example: 05evalTestOnCosmicRay.sh /home/auri/temp/lucca/python_experiments files.txt test-sets.txt"
	exit
fi

baseDir=$1
dataFile=$2
testSetFile=$3

tool=mutatest

# Iterando sobre o arquivo de test-sets
testSetData=$(cat "${baseDir}/${testSetFile}")
for tcDir in $testSetData
do
	echo "Processing test set: $tcDir"

	projectsData=$(cat "${baseDir}/${dataFile}")

	for project in $projectsData
	do
		prjArr=($(echo $project | tr ":" "\n"))
		prjDir="${prjArr[0]}"
		clazz="${prjArr[1]}"
		module="${clazz%%.*}"

		echo -e "\tProcessing program $clazz"
		cd "${baseDir}/${module}"

		# Cleaning previous report
		rm -rf ./${tcDir}/${tool}
		mkdir ./${tcDir}/${tool}

		/usr/bin/time -o ${tool}.time --quiet -p mutatest -s ${module}.py -t "python -m pytest --tb=no ./${tcDir}" -r 2023 -m f -o ${tcDir}/${tool}/${tcDir}-report.rst >& ${tool}.out

		mv ${tool}.time ${tool}.out ./${tcDir}/${tool}

		rm -rf .pytest_cache
		rm -rf __pycache__
		rm -rf ./${tcDir}/__pycache__
	done
done