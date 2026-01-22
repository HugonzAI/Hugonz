# 🛡️ 保护代码不被AI助手修改

## 问题
AI代码助手（GitHub Copilot, Cursor, etc.）会自动"优化"代码，破坏核心逻辑。

## 解决方案

### 方案1: 禁用AI助手（推荐）

**VS Code:**
1. 打开设置 (Ctrl+,)
2. 搜索 "Copilot"
3. 取消勾选 "Enable"

**Cursor:**
1. Settings → Cursor Settings
2. 禁用 "Auto-suggest" 或 "Auto-edit"

---

### 方案2: 排除特定文件

**在 `.gitignore` 同目录创建 `.cursorignore` 或 `.copilotignore`:**

```
# 保护核心文件不被AI修改
est_converter.py
esa615_connector.py
dta_to_csv_converter.py
esa615_ui_addon.py

# 保护模板文件
*.xlsx
```

---

### 方案3: 添加代码保护注释

在文件开头添加：

```python
# ⚠️ CRITICAL: DO NOT MODIFY - Protected baseline code
# This file contains protected functions that must not be changed
# Any AI-suggested changes should be rejected
```

---

### 方案4: 使用受保护的分支

只在受保护的分支编辑：
```bash
git checkout -b my-protected-branch
# 在这个分支工作，不要让AI助手改动
```

---

## ✅ 恢复干净的代码

如果代码被AI改坏了：

```bash
# 查看哪些文件被修改
git status

# 恢复单个文件到最后一次提交
git checkout -- est_converter.py

# 或者恢复所有文件
git reset --hard HEAD
```

---

## 🔒 下载受保护的版本

从GitHub下载最新的干净版本：
- Branch: claude/est-converter-baseline-sbRr5
- Commit: 65cb36e
- 确保没有本地修改

