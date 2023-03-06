#!/usr/bin/bash
#######################################################################
# Script that runs Mutatest mutation tool in a set of programs
#######################################################################

if (($# < 2))
then
	echo "error: evalTestOnMutatest.sh <project root dir> <test case directory>"
	echo "Example: evalTestOnMutatest.sh /home/auri/temp/lucca/python_experiments DYNAMOSA"
	exit
fi

baseDir=$1
tcDir=$2

tool=mutatest

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

	/usr/bin/time -o ${tool}.time --quiet -p mutatest -s ${module}.py -t "python -m pytest ./${tcDir}" -m f -o ${tcDir}/${tool}/${tcDir}-report.rst >& ${tool}.out

	mv ${tool}.time ${tool}.out ./${tcDir}/${tool}

	rm -rf .pytest_cache
	rm -rf __pycache__
	rm -rf ./${tcDir}/__pycache__
done