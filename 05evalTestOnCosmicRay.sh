#!/usr/bin/bash
#######################################################################
# Script that runs Cosmic.Ray mutation tool in a set of programs
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

tool=cosmic-ray

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

		# Generating cosmic configuration file
		echo "[cosmic-ray]" > ${module}.toml
		echo "module-path = \"${module}.py\"" >> ${module}.toml
		echo "timeout = 60.0" >> ${module}.toml
		echo "excluded-modules = []" >> ${module}.toml
		echo "test-command = \"python -m pytest --tb=no ./${tcDir}\"" >> ${module}.toml
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

		mv ${module}.sqlite ${tool}.time ${tool}.baseline ${tool}.out ./${tcDir}/${tool}

		rm -rf .pytest_cache
		rm -rf __pycache__
		rm -rf ./${tcDir}/__pycache__

		#Removing unfinished python -m pytest process
		pkill -f 'python -m pytest'
	done
done