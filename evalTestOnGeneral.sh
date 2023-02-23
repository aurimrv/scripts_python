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

	time mut.py -t ${module}.py -u ./${tcDir} --runner pytest --report-html ./${tcDir}/mutpy;

    time mutmut run --paths-to-mutate ${module}.py --tests-dir ./${algorithm}/test_${module}.py --runner "\"python3 -m pytest test_${module}.py\"";
    mutmut html;

    time mutatest -s ${module}.py -t pytest -m f -o ${algorithm}/mutatest/${algorithm}-report.rst;

    #echo ${module}.py > cosmic-config;
    #echo 20 >> cosmic-config;
    #echo 'python3 -m pytest test_${module}.py' >> cosmic-config;
    #echo 1 >> cosmic-config;
    #cosmic-ray new-config ${module}.toml < cosmic-config;
    #cosmic-ray init ${module}.toml ${module}.sqlite;
    #cosmic-ray exec ${module}.toml ${module}.sqlite;
    #cr-report ${module}.sqlite > report_cosmicray.html;
done
