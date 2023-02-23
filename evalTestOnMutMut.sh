#!/usr/bin/bash

if (($# < 2))
then
	echo "error: evalTestOnMutPy.py <project root dir> <test case directory>"
	echo "Example: evalTestOnMutPy.py /home/auri/temp/lucca/python_experiments DYNAMOSA"
	exit
fi

baseDir=$1
tcDir=$2

projectsData=$(cat "${baseDir}/files.txt")

for project in $projectsData
do
	prjArr=($(echo $project | tr ":" "\n"))
	prjDir="${prjArr[0]}"
	clazz="${prjArr[1]}"
	module="${clazz%%.*}"

	echo "Processing program $clazz"
	cd "${baseDir}/${module}"

	cmd="mut.py -e -m -c --debug -t ${module}.py -u ./${tcDir} --runner pytest --report-html ./${tcDir}/mutpy"

	/usr/bin/time -o mutpy.time --quiet -p $cmd >& mutpy.out

	mv mutpy.time mutpy.out ./${tcDir}/mutpy

	rm -rf __pycache__
	rm -rf ./${tcDir}/__pycache__
done