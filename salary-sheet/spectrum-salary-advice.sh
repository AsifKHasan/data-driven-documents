#!/usr/bin/env bash
# salary advice from data pipeline

set echo off

# parameters
ORG="spectrum"

# the scripts are in src directory
pushd ./src
./${ORG}-salary-advice-app.py

if [ ${?} -ne 0 ]; then
  popd && exit 1
else
  popd
fi
