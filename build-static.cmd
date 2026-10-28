@echo off
setlocal
set "ROOT=C:\FILES\PROJECTS\E2FSPROGS"
set "PATH=C:\msys64\mingw64\bin;C:\msys64\usr\bin;%PATH%"
"C:\msys64\mingw64\bin\gcc.exe" -O2 -static -static-libgcc "%ROOT%\native_probe.c" -o "%ROOT%\dist\native_probe_static.exe"
if errorlevel 1 exit /b 1
"%ROOT%\dist\native_probe_static.exe"
endlocal
