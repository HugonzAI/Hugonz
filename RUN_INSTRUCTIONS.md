# EST Converter - 运行指南

## 快速开始

### 方法1: 直接运行（开发/测试）

```bash
# 1. 进入目录
cd /home/user/Hugonz

# 2. 安装依赖（首次运行）
pip install PySide6 openpyxl python-dateutil

# 3. 可选：安装ESA615支持
pip install pyserial

# 4. 运行程序
python3 est_converter.py
```

### 方法2: Windows EXE打包

```bash
# 1. 安装PyInstaller
pip install pyinstaller

# 2. 运行打包脚本
python build_exe.py

# 3. 找到生成的EXE
# 位置: dist/EST_Converter.exe
# 双击即可运行
```

## 必需文件清单

✅ 以下文件必须与程序在同一目录：
- `est_converter.py` - 主程序
- `example_Good.xlsx` - 输出模板（重要！）
- `EST Tester.xlsx` - Tester映射表
- `EST_Limits_Summary.xlsx` - 固定限值表

✅ ESA615功能（可选）：
- `esa615_connector.py`
- `dta_to_csv_converter.py`
- `esa615_ui_addon.py`

## 使用流程

### 转换CSV文件：
1. 运行程序
2. 点击 "📁 CSV Files" 标签
3. 点击 "📄 Add Files" 添加CSV文件
4. 选择输出文件夹
5. 点击 "🚀 Convert Files to XLSX"

### 使用ESA615设备：
1. 运行程序
2. 连接ESA615设备（USB线）
3. 点击 "🔌 ESA615 Device" 标签
4. 选择COM端口（检查设备管理器）
5. 点击 "Connect"
6. 选择文件并下载

## 常见问题

### Q: 提示找不到模板文件
**A:** 确保 `example_Good.xlsx` 与程序在同一目录

### Q: COM端口访问被拒绝
**A:** 
- 以管理员身份运行
- 关闭其他使用COM端口的程序
- 重新插拔USB线

### Q: "No module named 'pyserial'"
**A:** 如果只转换CSV，可忽略。需要ESA615功能则：`pip install pyserial`

## 技术支持

- 查看 README.md 了解详细功能说明
- 查看 BUILD_EXE_GUIDE.md 了解打包详情
- 查看 UI_PREVIEW.md 了解界面设计
