# 🚨 紧急恢复指南 - AI污染代码修复

## 问题
AI助手（可能是GitHub Copilot Workspace、Cursor等）在GitHub仓库上直接修改了代码。

---

## 🔴 立即恢复 - 方案1：硬回滚到最后干净版本

```bash
# 1. 查看当前状态
git status
git log --oneline -10

# 2. 找出最后一个干净的commit（我的最后一次提交）
# 当前最新干净版本: 3afc416

# 3. 硬回滚（警告：会丢失所有本地修改）
git reset --hard 3afc416

# 4. 强制推送到远程（覆盖被污染的版本）
git push --force origin claude/est-converter-baseline-sbRr5
```

---

## 🔴 立即恢复 - 方案2：创建全新分支

```bash
# 1. 基于干净的commit创建新分支
git checkout -b claude/est-baseline-clean 3afc416

# 2. 推送新分支
git push -u origin claude/est-baseline-clean

# 3. 在新分支工作（放弃旧的被污染分支）
```

---

## 🛡️ 防止再次被污染

### 检查GitHub设置

1. **访问仓库设置**
   - Settings → General → Features
   - **禁用** "Copilot" 或 "AI features"

2. **检查GitHub Apps**
   - Settings → Integrations → Applications
   - 查看是否有自动化工具有写入权限
   - 撤销可疑应用的访问权限

3. **保护分支**
   - Settings → Branches → Add rule
   - Branch name pattern: `claude/*`
   - 勾选 "Require pull request reviews"
   - 勾选 "Lock branch"

### 检查本地Git配置

```bash
# 检查是否有自动化钩子
ls -la .git/hooks/

# 检查git配置
git config --list | grep -i copilot
git config --list | grep -i cursor
git config --list | grep -i ai
```

---

## 🔍 诊断：找出AI做的修改

```bash
# 查看最近20次提交
git log --all --format="%h %an %ae %s" -20

# 查看某个文件的修改历史
git log --oneline --all -- est_converter.py

# 对比两个版本的差异
git diff <旧commit> <新commit> est_converter.py
```

---

## 📤 发给我的信息

请运行以下命令并把输出发给我：

```bash
# 1. 当前分支和状态
git branch -a
git status

# 2. 最近的提交
git log --format="%h %an %s" -15

# 3. 检查核心文件
git log --oneline -10 -- est_converter.py

# 4. 如果有未提交的修改，显示差异
git diff est_converter.py | head -100
```

这样我能准确找出哪些提交是问题，帮你恢复到正确版本。

---

## ⚠️ 重要提醒

如果你正在使用：
- **GitHub Copilot Workspace**: 禁用它！
- **Cursor**: 关闭 "Auto-apply" 功能
- **GitHub Codespaces**: 检查AI设置
- **任何浏览器插件**: 可能有AI自动修改代码

**在恢复代码前，先关闭所有AI工具！**
