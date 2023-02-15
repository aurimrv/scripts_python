#!/usr/bin/bash

if (($# < 2))
then
	echo "error: mutatePynguin.py <project root dir> <algorithm>"
	echo "Example: mutatePynguin.py /home/auri/temp/lucca/python_experiments DYNAMOSA"
	exit
fi

baseDir=$1
algorithm=$2

projectsData=$(cat "${baseDir}/files.txt")

tcName="test_pynguin_${algorithm}.py"

for project in $projectsData
do
	prjArr=($(echo $project | tr ":" "\n"))
	prjDir="${prjArr[0]}"
	clazz="${prjArr[1]}"
	module="${clazz%%.*}"

	echo "Processing program $clazz"
	cd "${baseDir}/${module}"
    #cp ${module}.py ./${algorthm}
    #cd ./${algorthm}

	time mut.py -t ${module}.py -u ./${algorithm}/test_${module}.py --runner pytest --report-html ./${algorithm}/mutpy;

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
