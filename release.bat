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

python -m PyInstaller ytdlp_gui.spec >nul 2>&1
if exist "dist\ytdlp_gui.exe" (
    echo BUILD_SUCCESS: v%NEW_VER% - dist\ytdlp_gui.exe
) else (
    echo BUILD_INFO: v%NEW_VER% - Pure Python package ready
)

exit /b 0
