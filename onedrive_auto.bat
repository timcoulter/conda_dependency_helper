@echo off

:check_onedrive
echo Checking OneDrive synchronization status...

REM Construct path to dll which helps get sync status
set "userFolder=%USERPROFILE%"
set "dllPath=%userFolder%\OneDrive - James Cook University\scripts\conda_dependency_helper\OneDriveLib.dll"
set "scriptPath=%userFolder%\OneDrive - James Cook University\scripts\conda_dependency_helper"

REM Construct the path dynamically using environment variables
set "userProfilePath=%USERPROFILE%"
set "scriptPath=%userProfilePath%\OneDrive - James Cook University\scripts\conda_dependency_helper\update_conda_environments.py"


REM Add a delay to give OneDrive time to initialize
timeout /t 10 >nul

for /f "delims=" %%G in ('powershell -Command "Import-Module '%dllPath%'; Unblock-File '%dllPath%'; Import-Module '%dllPath%'; Get-ODStatus -ByPath '%scriptPath%'"') do (
    set "output=%%G"
)
echo Output: %output%

if "%output%"=="UpToDate" (
    python "%scriptPath%"
) else (
    echo OneDrive is not up to date. Retrying in 10 seconds...
    timeout /t 10 >nul
    goto check_onedrive
)
