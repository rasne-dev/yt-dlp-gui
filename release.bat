@echo off
setlocal enabledelayedexpansion

python bump_version.py
if %ERRORLEVEL% NEQ 0 (
    echo Error updating version.
    exit /b 1
)

set /p NEW_VER=<.version
del .version 2>nul

echo Build in progress for v%NEW_VER%...

if exist "dist\ytdlp_gui.exe" move /Y "dist\ytdlp_gui.exe" "%TEMP%\ytdlp_gui_prev.exe" >nul 2>&1

pyinstaller --noconfirm ytdlp_gui.spec >nul 2>&1
if exist "dist\ytdlp_gui.exe" (
    echo BUILD_SUCCESS: v%NEW_VER% - dist\ytdlp_gui.exe
) else (
    echo BUILD_FAILED: v%NEW_VER%
    exit /b 1
)

exit /b 0
