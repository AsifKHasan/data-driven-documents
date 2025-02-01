:: salary advice from data pipeline

@echo off

:: parameters
set ORG="cybernetics"

:: the scripts are in src directory
pushd src
python %ORG%-salary-advice-app.py

if errorlevel 1 (
  popd
  exit /b %errorlevel%
)

popd
