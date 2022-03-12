#!/usr/bin/env bash
# document from data pipeline

# parameters
ORG="sscl"
DOC=$1

set echo off

# the scripts are in src directory
pushd ./src
./${ORG}-${DOC}.py

if [ ${?} -ne 0 ]; then
  popd && exit 1
else
  popd
fi
