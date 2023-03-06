#!/usr/bin/bash
#######################################################################
# Script that runs MutMut mutation tool in a set of programs
#######################################################################

if (($# < 2))
then
	echo "error: evalTestOnMutMut.sh <project root dir> <test case directory>"
	echo "Example: evalTestOnMutMut.sh /home/auri/temp/lucca/python_experiments DYNAMOSA"
	exit
fi

baseDir=$1
tcDir=$2

tool=mutmut

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
	/usr/bin/time -o ${tool}.time --quiet -p mutmut run --paths-to-mutate ${module}.py --tests-dir ./${tcDir} --runner "python3 -m pytest ./${tcDir}" >& ${tool}.out

	mutmut html

	mv html ./${tcDir}/${tool}
	
	mv ${tool}.time ${tool}.out ./${tcDir}/${tool}

	rm .${tool}-cache
	rm -rf .pytest_cache
	rm -rf __pycache__
	rm -rf ./${tcDir}/__pycache__
done