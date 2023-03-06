#!/usr/bin/bash

if (($# < 1))
then
	echo "error: parsePynguinRunAll.sh <project root dir>"
	echo "Example: parsePynguinRunAll.sh /home/auri/temp/lucca/python_experiments"
	exit
fi

baseDir=$1
scriptDir=${baseDir}/scripts
algorithm1="DYNAMOSA"
algorithm2="MOSA"
algorithm3="MIO"
algorithm4="WHOLE_SUITE"
algorithm5="RANDOM"

${scriptDir}/parsePynguin.sh $baseDir $algorithm1
${scriptDir}/parsePynguin.sh $baseDir $algorithm2
${scriptDir}/parsePynguin.sh $baseDir $algorithm3
${scriptDir}/parsePynguin.sh $baseDir $algorithm4
#${scriptDir}/parsePynguin.sh $baseDir $algorithm5