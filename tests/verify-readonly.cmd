@echo off
setlocal
set "ROOT=C:\FILES\PROJECTS\E2FSPROGS"
set "BACKUP=C:\Users\User\Desktop\REDMAGIC_NX709S_backup"
if not exist "%ROOT%\artifacts\e2fsck.exe" exit /b 1
"%ROOT%\artifacts\e2fsck.exe" -fn "%BACKUP%\system_b_original.img"
if errorlevel 1 exit /b 1
"%ROOT%\artifacts\e2fsck.exe" -fn "%BACKUP%\product_b_original.img"
if errorlevel 1 exit /b 1
"%ROOT%\artifacts\debugfs.exe" -R "stat /media/audio/ui/camera_click.ogg" "%BACKUP%\product_b_original.img"
if errorlevel 1 exit /b 1
"%ROOT%\artifacts\debugfs.exe" -R "stat /system/media/audio/ui/camera_click.ogg" "%BACKUP%\system_b_original.img"
if errorlevel 1 exit /b 1
echo Read-only checks completed. No -w or repair options used.
exit /b 0
