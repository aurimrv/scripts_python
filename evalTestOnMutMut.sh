#!/usr/bin/bash
#######################################################################
# Script that runs MutMut mutation tool in a set of programs
#######################################################################

if (($# < 2))
then
	echo "error: evalTestOnCosmicRay.sh <project root dir> <test-set-file>"
	echo "Example: evalTestOnCosmicRay.sh /home/auri/temp/lucca/python_experiments test-sets.txt"
	exit
fi

baseDir=$1
testSetFile=$2

tool=mutmut

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

		# MutMut execution command line
		/usr/bin/time -o ${tool}.time --quiet -p mutmut run --paths-to-mutate ${module}.py --tests-dir ./${tcDir} --runner "python3 -m pytest --tb=no ./${tcDir}" >& ${tool}.out

		mutmut html

		mv html ./${tcDir}/${tool}
		
		mv ${tool}.time ${tool}.out ./${tcDir}/${tool}

		rm .${tool}-cache
		rm -rf .pytest_cache
		rm -rf __pycache__
		rm -rf ./${tcDir}/__pycache__
	done
done