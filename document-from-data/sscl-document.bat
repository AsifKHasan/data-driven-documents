:: document from data pipeline

@echo off

:: parameters
set ORG="sscl"
set DOC=%1

:: the scripts are in src directory
pushd src
%ORG%-%DOC%.py

if errorlevel 1 (
  popd
  exit /b %errorlevel%
)

popd
