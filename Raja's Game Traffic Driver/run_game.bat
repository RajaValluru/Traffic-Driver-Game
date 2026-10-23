@echo off
rem Launches the frozen exe. Rebuild after code changes with:  python setup.py build
cd "%~dp0build\exe.win-amd64-3.12"
start "" "cargame.exe"
