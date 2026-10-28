@echo off
setlocal EnableExtensions
for %%I in ("%~dp0..") do set "ROOT=%%~fI"
set "BIN=%ROOT%\artifacts\beta-candidate"
set "E2FSPROGS_BIN=%BIN%"
set "E2FSPROGS_MKE=%BIN%\mke2fs.exe"
set "PYTHON=C:\Users\User\AppData\Local\Programs\Python\Python314\python.exe"
if not exist "%PYTHON%" set "PYTHON=python.exe"
if not exist "%BIN%\e2fsck.exe" exit /b 2
for %%T in (test_native_ext4.py test_beta_matrix.py test_repair_inode.py test_beta_qualification.py test_shared_blocks_guard.py test_independent_windows.py test_independent_negative.py) do (
    echo Testing %%T
    "%PYTHON%" "%ROOT%\tests\%%T" > "%BIN%\%%T.log" 2>&1
    if errorlevel 1 (
        type "%BIN%\%%T.log"
        echo FAILED %%T
        exit /b 1
    )
    echo PASS %%T
)
echo ALL TESTS PASSED
exit /b 0
