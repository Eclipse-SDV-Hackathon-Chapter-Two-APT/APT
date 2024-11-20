#!/bin/bash
set -e

# mosaic
dir_tools=tools
tmp=`ls ${dir_tools} | grep scenario-convert-.*.jar`
tools=${dir_tools}/${tmp//[^A-Za-z0-9\-\.]}

# create and run command
cmd="java -cp ${tools}:lib/mosaic/*:lib/extended/*:lib/third-party/* com.dcaiti.mosaic.tools.scenarioconvert.core.Starter $*"
$cmd