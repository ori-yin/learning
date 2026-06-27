# OpenClaw 安装指南（Windows）

> 一份详细的 OpenClaw 本地安装配置指南

---

## 前置要求

### 1. 安装 Node.js

访问官网下载并安装：https://nodejs.org/zh-cn/download

- 推荐下载 **LTS 版本**（长期支持版）
- 安装时保持默认选项即可
- 安装完成后，打开命令行验证：
  ```powershell
  node -v
  npm -v
  ```

### 2. 安装 Git

访问官网下载并安装：https://git-scm.com/install/windows

- 安装时保持默认选项
- 安装完成后验证：
  ```powershell
  git --version
  ```

---

## 安装 OpenClaw

### 步骤 1：设置 PowerShell 执行策略

以**当前用户**权限设置执行策略（不需要管理员权限）：

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

输入 `Y` 确认。

### 步骤 2：配置 npm 镜像源（可选但推荐）

使用国内镜像源加速安装：

```powershell
npm config set registry https://registry.npmmirror.com
```

### 步骤 3：运行安装脚本

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

等待安装完成。

---

## 配置与启动

### 步骤 4：初始化配置

```powershell
openclaw config
```

按照提示完成配置：
- 选择模型提供商（如 Qwen、OpenAI 等）
- 输入 API Key（如果需要）
- 设置工作区路径

### 步骤 5：启动 Gateway

```powershell
openclaw gateway run
```

Gateway 启动后，会监听本地端口。

### 步骤 6：打开控制台

```powershell
openclaw dashboard
```

这会打开浏览器，进入 OpenClaw 的 Web 控制台，可以开始对话。

---

## 常用命令

| 命令 | 说明 |
|------|------|
| `openclaw status` | 查看运行状态 |
| `openclaw gateway restart` | 重启 Gateway |
| `openclaw gateway stop` | 停止 Gateway |
| `openclaw doctor` | 诊断问题 |
| `openclaw --help` | 查看所有命令 |

---

## 常见问题

### 1. 安装脚本报错

**错误：** `无法加载文件，因为在此系统上禁止运行脚本`

**解决：** 重新执行步骤 1 的 PowerShell 策略设置命令。

### 2. npm 安装超时

**解决：** 确保已配置国内镜像源（步骤 2），或检查网络连接。

### 3. Gateway 启动失败

**排查：**
- 检查端口是否被占用
- 查看日志：`openclaw gateway status`
- 尝试重启：`openclaw gateway restart`

### 4. 模型无法连接

**排查：**
- 检查 API Key 是否正确
- 确认网络连接正常
- 查看 `openclaw config` 中的配置

---

## 工作区说明

OpenClaw 的工作区默认位于：
- Windows: `C:\Users\<用户名>\.openclaw\workspace`

可以在配置中自定义工作区路径。

工作区文件说明：
- `SOUL.md` - AI 人格设定
- `USER.md` - 用户信息
- `IDENTITY.md` - 身份定义
- `MEMORY.md` - 长期记忆
- `memory/` - 日常记忆文件夹

---

## 参考资料

- 官方文档：https://docs.openclaw.ai
- GitHub: https://github.com/openclaw/openclaw
- 社区：https://discord.com/invite/clawd

---

_最后更新：2026-03-14_
