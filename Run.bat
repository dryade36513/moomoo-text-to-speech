@echo off
setlocal enabledelayedexpansion
chcp 65001 > nul

if not exist "venv\Scripts\activate.bat" (
    python -m venv venv
)

call venv\Scripts\activate.bat
pip install gradio edge-tts

python app.py
pause
