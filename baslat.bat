@echo off
python ytdlp_gui.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Uygulama baslatilamadi. Python'un kurulu ve PATH'e ekli oldugundan emin olun.
    pause
)
