@echo off
title Civilization IV: Beyond the Sword - Restore Original English
chcp 65001 >nul

:: Check for Administrator privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [提示] 正在請求系統管理員權限...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0PatchFiles\uninstall.ps1"

echo.
echo 請按任意鍵關閉視窗...
pause >nul
