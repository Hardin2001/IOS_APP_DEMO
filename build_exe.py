#!/usr/bin/env python3
"""
HUD Settings 应用程序打包脚本
自动化创建可执行文件
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def clean_build_files():
    """清理之前的构建文件"""
    print("🧹 清理构建文件...")
    
    # 删除构建目录
    build_dirs = ['build', 'dist', '__pycache__']
    for dir_name in build_dirs:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   删除: {dir_name}")
    
    # 删除spec文件
    spec_files = [f for f in os.listdir('.') if f.endswith('.spec')]
    for spec_file in spec_files:
        os.remove(spec_file)
        print(f"   删除: {spec_file}")

def create_icon():
    """创建应用图标"""
    print("🎨 创建应用图标...")
    
    # 创建一个简单的ICO图标文件
    icon_content = """
    我们将使用PyInstaller的默认图标，或者你可以提供自己的.ico文件
    """
    
    # 这里可以添加创建图标的代码
    return None

def build_application():
    """构建应用程序"""
    print("🔨 开始构建应用程序...")
    
    # PyInstaller 命令参数
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',                    # 创建单个exe文件
        '--windowed',                   # 无控制台窗口
        '--name=HUD_Settings',          # 应用程序名称
        '--add-data=fonts;fonts',       # 包含字体文件（如果有）
        '--hidden-import=PIL',          # 隐式导入PIL
        '--hidden-import=PIL._tkinter_finder',
        '--hidden-import=customtkinter',
        '--collect-all=customtkinter',  # 收集customtkinter所有文件
        '--noconfirm',                  # 不询问覆盖
        'main.py'                       # 主文件
    ]
    
    print(f"执行命令: {' '.join(cmd)}")
    
    try:
        # 运行PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ 构建成功!")
        print(result.stdout)
        return True
        
    except subprocess.CalledProcessError as e:
        print("❌ 构建失败!")
        print(f"错误代码: {e.returncode}")
        print(f"错误输出: {e.stderr}")
        print(f"标准输出: {e.stdout}")
        return False

def create_batch_file():
    """创建启动批处理文件"""
    print("📝 创建启动脚本...")
    
    batch_content = '''@echo off
title HUD Settings Launcher
echo 启动 HUD Settings 应用程序...
echo.

REM 检查exe文件是否存在
if not exist "dist\\HUD_Settings.exe" (
    echo ❌ 错误: 找不到 HUD_Settings.exe 文件
    echo 请确保构建成功完成
    pause
    exit /b 1
)

REM 启动应用程序
echo ✅ 启动应用程序...
start "" "dist\\HUD_Settings.exe"

REM 等待一下确保启动
timeout /t 2 /nobreak >nul

echo ✅ 应用程序已启动!
echo 如果遇到问题，请检查dist文件夹中的HUD_Settings.exe
pause
'''
    
    with open('run_hud.bat', 'w', encoding='utf-8') as f:
        f.write(batch_content)
    
    print("   创建: run_hud.bat")

def main():
    """主函数"""
    print("🚀 HUD Settings 应用程序打包工具")
    print("=" * 50)
    
    # 检查是否在正确的目录
    if not os.path.exists('main.py'):
        print("❌ 错误: 找不到 main.py 文件")
        print("请确保在项目根目录运行此脚本")
        return False
    
    try:
        # 步骤1: 清理构建文件
        clean_build_files()
        
        # 步骤2: 构建应用程序
        if not build_application():
            return False
        
        # 步骤3: 创建启动脚本
        create_batch_file()
        
        # 完成信息
        print("\n" + "=" * 50)
        print("🎉 打包完成!")
        print("\n📁 文件位置:")
        print("   • 可执行文件: dist/HUD_Settings.exe")
        print("   • 启动脚本: run_hud.bat")
        
        print("\n🎯 使用方法:")
        print("   1. 双击 run_hud.bat 启动应用")
        print("   2. 或直接运行 dist/HUD_Settings.exe")
        
        print("\n📦 分发:")
        print("   • 将整个 dist 文件夹分享给其他人")
        print("   • 或仅分享 HUD_Settings.exe (推荐)")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 构建过程中出错: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        input("\n按Enter键退出...")
        sys.exit(1)
    else:
        input("\n按Enter键退出...")