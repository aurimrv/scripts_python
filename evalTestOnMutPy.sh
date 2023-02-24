#!/usr/bin/bash

if (($# < 2))
then
	echo "error: evalTestOnMutPy.py <project root dir> <test case directory>"
	echo "Example: evalTestOnMutPy.py /home/auri/temp/lucca/python_experiments DYNAMOSA"
	exit
fi

baseDir=$1
tcDir=$2

tool=mutpy

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

	cmd="mut.py -e -m -c --debug -t ${module}.py -u ./${tcDir} --runner pytest --report-html ./${tcDir}/${tool}"

	/usr/bin/time -o ${tool}.time --quiet -p $cmd >& ${tool}.out

	mv ${tool}.time ${tool}.out ./${tcDir}/${tool}

	rm -rf __pycache__
	rm -rf ./${tcDir}/__pycache__
done