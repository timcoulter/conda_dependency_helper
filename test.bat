@echo off

for /f "delims=" %%G in ('powershell -Command "Import-Module 'C:\Users\Tim\OneDrive - James Cook University\Postgraduate\Python Scripts\conda_dependency_helper\OneDriveLib.dll'; Unblock-File 'C:\Users\Tim\OneDrive - James Cook University\Postgraduate\Python Scripts\conda_dependency_helper\OneDriveLib.dll'; Import-Module 'C:\Users\Tim\OneDrive - James Cook University\Postgraduate\Python Scripts\conda_dependency_helper\OneDriveLib.dll'; Get-ODStatus -ByPath 'C:\Users\Tim\OneDrive - James Cook University\Postgraduate\Python Scripts\conda_dependency_helper'"') do (
    set "output=%%G"
)

echo Output: %output%

pause