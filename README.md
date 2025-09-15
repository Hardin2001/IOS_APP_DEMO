# 🚗 HUD Settings 应用程序

## 📦 文件说明

### 🎯 主要文件
- **`dist/HUD_Settings.exe`** - 主程序，双击即可运行
- **`run_hud.bat`** - 启动脚本（可选）

### 📁 完整文件列表
```
HUDAPP/
├── dist/
│   └── HUD_Settings.exe        # ⭐ 主程序文件
├── main_clean.py               # 源代码（干净版本）
├── build_exe.py                # 打包脚本
├── run_hud.bat                 # 启动脚本
└── README.md                   # 本说明文件
```

## 🚀 使用方法

### 方法1：直接运行（推荐）
1. 找到 `dist` 文件夹
2. 双击 `HUD_Settings.exe`
3. 应用程序会立即启动

### 方法2：使用启动脚本
1. 双击 `run_hud.bat`
2. 脚本会自动启动应用程序

## ✨ 功能介绍

### 🎛️ HUD控制功能
- **Rear Traffic Alert** - 后方交通警报
- **Headlight Status** - 前照灯状态
- **Turn Signals** - 转向信号
- **Navigation** - 导航信息
- **Speed Limits** - 速度限制
- **Takeover Alerts** - 接管警告
- **Lane Departure** - 车道偏离
- **Autopilot Status** - 自动驾驶状态
- **Gear Position** - 档位显示
- **Battery Range** - 电池续航
- **Speed Display** - 速度显示

### 🎨 主题选择
- **Dark** - 深色主题（默认）
- **Light** - 浅色主题
- **Nature** - 自然绿色主题
- **Cyber** - 赛博蓝色主题

### 🔄 同步功能
- 点击 "Sync to Device" 将设置同步到目标设备

## 📱 界面特点

- **iPhone风格设计** - 模仿iOS界面风格
- **现代化UI** - 使用customtkinter实现圆角、阴影等效果
- **响应式布局** - 自适应不同屏幕尺寸
- **流畅动画** - 开关切换有平滑动画效果

## 🔧 技术规格

- **运行环境**: Windows 10/11
- **无需安装**: 单文件exe，开箱即用
- **文件大小**: 约 50-80MB
- **内存占用**: 约 50-100MB
- **启动时间**: 2-5秒

## 📦 分发说明

### 🎁 分享给其他人
1. **完整分发**: 分享整个 `dist` 文件夹
2. **简洁分发**: 仅分享 `HUD_Settings.exe` 文件（推荐）

### 💾 系统要求
- Windows 10 或更高版本
- 至少 100MB 可用磁盘空间
- 至少 4GB 系统内存

## 🛠️ 开发信息

### 📝 源代码
- 主程序: `main_clean.py`
- 框架: Python + customtkinter
- 打包工具: PyInstaller

### 🔄 重新打包
如果需要修改代码并重新打包：
```bash
# 1. 修改 main_clean.py
# 2. 运行打包脚本
python build_exe.py
```

## 🆘 故障排除

### ❌ 程序无法启动
1. 确保Windows系统为最新版本
2. 检查杀毒软件是否阻止运行
3. 右键exe文件 → 属性 → 解除阻止

### 🐌 启动缓慢
- 首次运行较慢是正常现象
- 后续启动会显著加快

### 💡 界面显示异常
- 确保系统DPI设置为100%或125%
- 更新显卡驱动程序

## 📞 技术支持

如遇到问题，请提供以下信息：
- 操作系统版本
- 错误信息截图
- 操作步骤描述

---

**版本**: 1.0.0  
**更新日期**: 2025年9月15日  
**兼容性**: Windows 10/11  