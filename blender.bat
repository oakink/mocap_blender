@echo off
set WORKSPACE_HOME=%~dp0
set PYTHONPATH=%PYTHONPATH%;%WORKSPACE_HOME%\package;%WORKSPACE_HOME%\startup
set BLENDER_SYSTEM_SCRIPTS=%WORKSPACE_HOME%\startup;%BLENDER_SYSTEM_SCRIPTS%
blender.exe -con --log-level -1 --python %WORKSPACE_HOME%\startup\startup.py