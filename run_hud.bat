@echo off
title HUD Settings Launcher
echo 启动 HUD Settings 应用程序...
echo.

REM 检查exe文件是否存在
if not exist "dist\HUD_Settings.exe" (
    echo ❌ 错误: 找不到 HUD_Settings.exe 文件
    echo 请确保构建成功完成
    pause
    exit /b 1
)

REM 启动应用程序
echo ✅ 启动应用程序...
start "" "dist\HUD_Settings.exe"

REM 等待一下确保启动
timeout /t 2 /nobreak >nul

echo ✅ 应用程序已启动!
echo 如果遇到问题，请检查dist文件夹中的HUD_Settings.exe
pause
