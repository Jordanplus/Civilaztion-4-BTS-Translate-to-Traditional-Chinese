@echo off
title Civilization IV: Beyond the Sword - Traditional Chinese Patch Installer
chcp 65001 >nul

:: Check for Administrator privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [提示] 正在請求系統管理員權限以寫入遊戲目錄...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0PatchFiles\install.ps1"

echo.
echo 請按任意鍵關閉視窗...
pause >nul
