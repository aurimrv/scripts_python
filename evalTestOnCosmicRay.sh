#!/usr/bin/bash

if (($# < 2))
then
	echo "error: evalTestOnMutatest.py <project root dir> <test case directory>"
	echo "Example: evalTestOnMutatest.py /home/auri/temp/lucca/python_experiments DYNAMOSA"
	exit
fi

baseDir=$1
tcDir=$2

tool=cosmic-ray

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

	# Generating cosmic configuration file
	echo "[cosmic-ray]" > ${module}.toml
	echo "module-path = \"${module}.py\"" >> ${module}.toml
	echo "timeout = 20.0" >> ${module}.toml
	echo "excluded-modules = []" >> ${module}.toml
	echo "test-command = \"python -m pytest ./${tcDir}\"" >> ${module}.toml
	echo "" >> ${module}.toml
	echo "[cosmic-ray.distributor]" >> ${module}.toml
	echo "name = \"local\"" >> ${module}.toml

    # Running cosmic registering the time 
    #cosmic-ray new-config ${module}.toml
    cosmic-ray init ${module}.toml ${module}.sqlite
    cosmic-ray --verbosity INFO baseline ${module}.toml >& ${tool}.baseline

    # Only executes if no test errors
	if [ $? -eq 0 ]
	then 
	    /usr/bin/time -o ${tool}.time --quiet -p cosmic-ray exec ${module}.toml ${module}.sqlite >& ${tool}.out
	    cr-report ${module}.sqlite --show-pending >& ./${tcDir}/${tool}/report_cosmicray.txt
	    cr-html ${module}.sqlite > ./${tcDir}/${tool}/report_cosmicray.html
	else 
	  echo "Error on test cases. Please, check ${tool}.baseline" 
	fi

	mv ${tool}.time ${tool}.baseline ${tool}.out ./${tcDir}/${tool}

	rm -rf .pytest_cache
	rm -rf __pycache__
	rm -rf ./${tcDir}/__pycache__
done