# OpenClaw 完全使用指南 🦞

> 你的第二大脑，这次它真的记得你把东西放哪儿了。

本指南涵盖 OpenClaw 的所有常用命令、配置方法和最佳实践。本文档为AI撰写，最新命令参考https://docs.openclaw.ai/zh-CN

---

## 📖 目录

- [快速开始](#-快速开始)
- [核心概念](#-核心概念)
- [Gateway 管理](#-gateway-管理)
- [Agent 管理](#-agent-管理)
- [频道配置](#-频道配置)
- [API/模型配置](#-api 模型配置)
- [定时任务](#-定时任务)
- [记忆系统](#-记忆系统)
- [插件管理](#-插件管理)
- [故障排查](#-故障排查)
- [常见问题](#-常见问题)

---

## 🚀 快速开始

### 第一次使用

```bash
# 1. 启动配置向导
openclaw configure

# 2. 启动 Gateway 服务
openclaw gateway start

# 3. 打开控制面板
openclaw dashboard

# 4. 检查系统状态
openclaw gateway status
```

### 每日必用命令

| 命令 | 说明 |
|------|------|
| `openclaw dashboard` | 打开 Web 控制面板 |
| `openclaw gateway status` | 查看服务状态 |
| `openclaw sessions` | 查看历史会话 |
| `openclaw doctor` | 健康检查 |

---

## 💡 核心概念

### Gateway vs Agent vs Channel

```
┌─────────────────────────────────────────────────────────┐
│                    OpenClaw 架构                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │   Channel   │───▶│   Gateway   │◀───│   Channel   │ │
│  │  (WhatsApp) │    │  (WebSocket)│    │  (Telegram) │ │
│  └─────────────┘    └──────┬──────┘    └─────────────┘ │
│                            │                            │
│                            ▼                            │
│                    ┌─────────────┐                      │
│                    │    Agent    │                      │
│                    │  (AI 大脑)   │                      │
│                    └─────────────┘                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

- **Gateway**：WebSocket 服务器，负责消息路由和调度
- **Agent**：AI 助手实例，处理对话和任务
- **Channel**：聊天频道（WhatsApp、Telegram、飞书等）

### Gateway 命令区别（重要！）

| 命令 | 运行方式 | 适用场景 | 关闭终端后 |
|------|----------|----------|------------|
| `openclaw gateway run` | **前景运行**，占用当前终端 | 调试、开发、查看实时日志 | ❌ 服务停止 |
| `openclaw gateway start` | **后台服务**，注册为系统任务 | 日常使用、生产环境 | ✅ 继续运行 |
| `openclaw gateway restart` | 重启后台服务 | 配置变更后 | ✅ 继续运行 |
| `openclaw gateway stop` | 停止后台服务 | 维护、关闭 | ❌ 服务停止 |

```bash
# 📌 推荐用法：
# 日常使用：启动后台服务（开机自启）
openclaw gateway start

# 调试时：前景运行（可以看到实时日志）
openclaw gateway run --verbose

# 配置变更后：重启服务
openclaw gateway restart
```

### 服务类型区别

| 服务类型 | 说明 | 命令 |
|----------|------|------|
| **前景运行** | 在当前终端运行，关闭终端即停止 | `gateway run` |
| **后台服务** | 注册为系统服务（Windows 任务计划/Linux systemd） | `gateway start` |
| **开发模式** | 使用独立配置目录（~/.openclaw-dev） | `openclaw --dev gateway run` |

---

## 🎛️ Gateway 管理

### 启动/停止

```bash
# 启动后台服务（推荐日常使用）
openclaw gateway start

# 前景运行（调试用，可看到实时日志）
openclaw gateway run

# 前景运行 + 详细日志
openclaw gateway run --verbose

# 重启服务
openclaw gateway restart

# 停止服务
openclaw gateway stop

# 查看服务状态
openclaw gateway status

# 卸载服务（保留配置）
openclaw gateway uninstall
```

### 高级选项

```bash
# 强制启动（杀死占用端口的进程）
openclaw gateway start --force

# 指定端口
openclaw gateway run --port 18790

# 开发模式（独立配置）
openclaw --dev gateway run

# 查看 Gateway 日志
openclaw logs

# 探测 Gateway 可达性
openclaw gateway probe
```

### 端口说明

| 模式 | 默认端口 | 说明 |
|------|----------|------|
| 标准模式 | 18789 | 生产环境 |
| 开发模式 | 19001 | `--dev` 模式 |
| 自定义 | 任意 | `--port <端口>` |

---

## 🤖 Agent 管理

### 什么是 Agent？

Agent 是独立的 AI 助手实例。你可以创建多个 Agent，每个有不同的：
- 工作区目录
- API 密钥配置
- 模型偏好
- 记忆系统

### 基本命令

```bash
# 列出所有 Agent
openclaw agents list

# 创建新 Agent
openclaw agents add my-assistant

# 删除 Agent
openclaw agents delete my-assistant

# 设置 Agent 身份（名称/头像/表情）
openclaw agents set-identity my-assistant

# 查看 Agent 的会话
openclaw sessions --agent my-assistant
```

### 多 Agent 使用场景

| 场景 | 建议 |
|------|------|
| 个人使用 | 1 个 Agent（default） |
| 工作/生活分离 | 2 个 Agent（work + personal） |
| 测试不同模型 | 多个 Agent 配置不同 API |
| 团队协作 | 每个成员独立 Agent |

---

## 📱 频道配置

### 支持的频道

| 频道 | 命令 | 说明 |
|------|------|------|
| WhatsApp | `channels login --channel whatsapp` | 扫码登录 |
| Telegram | `channels add --channel telegram --token <bot-token>` | Bot Token |
| 飞书/Lark | 插件安装 | 企业应用配置 |
| Discord | 插件安装 | Bot Token |

### 添加频道

```bash
# 列出已配置的频道
openclaw channels list

# WhatsApp（扫码登录）
openclaw channels login --channel whatsapp

# Telegram（需要 Bot Token）
# 1. 找 @BotFather 创建 Bot
# 2. 获取 Token
openclaw channels add --channel telegram --token 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

# 查看频道状态
openclaw channels status

# 深度检查（含认证状态）
openclaw channels status --deep

# 移除频道
openclaw channels remove <channel-id>
```

### 频道故障排查

```bash
# 查看频道日志
openclaw channels logs

# 解析用户/群组名称到 ID
openclaw channels resolve

# 查看频道能力（支持的功能）
openclaw channels capabilities
```

---

## 🔑 API/模型配置

### 配置 API 密钥

```bash
# 启动交互式配置向导
openclaw configure

# 或手动配置模型
openclaw config set agents.defaults.model.primary qwen-portal/coder-model
```

### 配置文件位置

| 文件 | 路径 | 说明 |
|------|------|------|
| 主配置 | `~/.openclaw/openclaw.json` | 全局配置 |
| Agent 配置 | `~/.openclaw/agents/<id>/agent/auth-profiles.json` | API 密钥 |
| 工作区 | `~/.openclaw/workspace` | 用户文件 |

### 添加新 API 提供商

编辑 `~/.openclaw/openclaw.json`，在 `models.providers` 中添加：

```json
{
  "models": {
    "providers": {
      "openai": {
        "baseUrl": "https://api.openai.com/v1",
        "apiKey": "sk-xxx",
        "api": "openai-completions",
        "models": [
          {
            "id": "gpt-4",
            "name": "GPT-4",
            "contextWindow": 128000,
            "maxTokens": 4096
          }
        ]
      }
    }
  }
}
```

### 切换模型

```bash
# 查看当前模型配置
openclaw config get agents.defaults.model

# 设置主模型
openclaw config set agents.defaults.model.primary moonshot/kimi-k2.5

# 设置备用模型（故障自动切换）
openclaw config set agents.defaults.model.fallbacks '["qwen-portal/vision-model", "xiaomi/mimo-v2-flash"]'
```

### 常用模型别名

| 别名 | 完整 ID | 提供商 |
|------|---------|--------|
| `qwen` | `qwen-portal/coder-model` | 通义千问 |
| `Kimi` | `moonshot/kimi-k2.5` | 月之暗面 |
| `Xiaomi` | `xiaomi/mimo-v2-flash` | 小米 |

---

## ⏰ 定时任务

### 什么是 Cron？

定时任务可以让你定期执行操作，比如：
- 每天早晨检查日历
- 每小时检查邮件
- 每周生成报告

### 基本命令

```bash
# 列出所有定时任务
openclaw cron list

# 查看调度器状态
openclaw cron status

# 添加定时任务（交互式）
openclaw cron add

# 立即运行任务（测试用）
openclaw cron run <job-id>

# 查看任务运行历史
openclaw cron runs <job-id>
```

### 创建定时任务示例

```bash
# 添加一个每天早晨 8 点的提醒
openclaw cron add
# 然后按提示输入：
# - 名称：morning-reminder
# - 调度：cron 表达式 "0 8 * * *"
# - 任务：systemEvent 或 agentTurn
```

### Cron 表达式参考

| 表达式 | 说明 |
|--------|------|
| `0 8 * * *` | 每天 8:00 |
| `0 */2 * * *` | 每 2 小时 |
| `0 9 * * 1-5` | 工作日 9:00 |
| `0 0 * * 0` | 每周日 0:00 |

### 启用/禁用任务

```bash
# 禁用任务（不删除）
openclaw cron disable <job-id>

# 启用任务
openclaw cron enable <job-id>

# 编辑任务
openclaw cron edit <job-id>

# 删除任务
openclaw cron rm <job-id>
```

---

## 🧠 记忆系统

### 记忆文件结构

```
~/.openclaw/workspace/
├── MEMORY.md              # 长期记忆（ curated ）
├── memory/
│   ├── 2026-03-11.md      # 每日笔记
│   ├── 2026-03-12.md
│   └── ...
└── HEARTBEAT.md           # 心跳任务配置
```

### 基本命令

```bash
# 搜索记忆
openclaw memory search "会议记录"

# 限制结果数量
openclaw memory search --query "项目" --max-results 10

# 查看记忆索引状态
openclaw memory status

# 深度检查（含嵌入模型）
openclaw memory status --deep

# 重新索引记忆文件
openclaw memory index

# 强制完全重新索引
openclaw memory index --force
```

### 记忆搜索配置

记忆搜索需要嵌入模型（Embedding）。配置方法：

1. 设置嵌入模型 API 密钥（OpenAI/Voyage/Mistral 等）
2. 或使用本地嵌入模型

```bash
# 检查嵌入模型状态
openclaw memory status --deep

# 如未配置，按提示设置 API 密钥
```

---

## 🔌 插件管理

### 安装插件

```bash
# 从 npm 安装
openclaw plugins install @openclaw/feishu

# 从本地路径安装
openclaw plugins install ./my-plugin

# 从压缩包安装
openclaw plugins install ./plugin.zip
```

### 管理插件

```bash
# 列出已发现的插件
openclaw plugins list

# 查看插件详情
openclaw plugins info feishu

# 启用插件
openclaw plugins enable feishu

# 禁用插件
openclaw plugins disable feishu

# 更新插件（npm 安装）
openclaw plugins update

# 卸载插件
openclaw plugins uninstall feishu

# 检查插件问题
openclaw plugins doctor
```

### 内置插件 vs 扩展插件

| 类型 | 位置 | 说明 |
|------|------|------|
| 内置插件 | `node_modules/openclaw/plugins` | 随主程序安装 |
| 扩展插件 | `~/.openclaw/extensions` | 用户安装 |

---

## 🔧 故障排查

### 诊断命令

```bash
# 完整健康检查（推荐首选）
openclaw doctor

# 非交互式诊断
openclaw doctor --non-interactive

# 查看系统状态
openclaw status

# 查看 Gateway 健康
openclaw gateway health

# 探测 Gateway
openclaw gateway probe
```

### 常见问题

#### Gateway 无法启动

```bash
# 1. 检查端口占用
netstat -ano | findstr :18789

# 2. 强制启动
openclaw gateway start --force

# 3. 查看详细日志
openclaw gateway run --verbose

# 4. 运行诊断
openclaw doctor
```

#### 频道无法连接

```bash
# 1. 查看频道状态
openclaw channels status --deep

# 2. 查看频道日志
openclaw channels logs

# 3. 重新登录
openclaw channels logout --channel <channel>
openclaw channels login --channel <channel>
```

#### 记忆搜索不工作

```bash
# 1. 检查嵌入模型配置
openclaw memory status --deep

# 2. 重新索引
openclaw memory index --force

# 3. 检查 API 密钥
openclaw config get auth.profiles
```

### 日志查看

```bash
# 查看 Gateway 日志
openclaw logs

# 查看实时日志（前景运行）
openclaw gateway run --verbose

# 查看频道日志
openclaw channels logs
```

---

## ❓ 常见问题

### Q: Gateway run 和 Gateway start 有什么区别？

**A:** 
- `run` = 前景运行，占用当前终端，关闭终端服务就停了
- `start` = 后台服务，注册为系统任务，关闭终端继续运行

**推荐**：日常使用 `start`，调试时用 `run`

### Q: 如何更换 API 提供商？

**A:** 三种方法：

1. **交互式配置**（推荐新手）
   ```bash
   openclaw configure
   ```

2. **命令行配置**
   ```bash
   openclaw config set agents.defaults.model.primary moonshot/kimi-k2.5
   ```

3. **手动编辑配置文件**
   编辑 `~/.openclaw/openclaw.json` 中的 `models.providers`

### Q: 如何创建多个 Agent？

**A:**
```bash
# 创建工作 Agent
openclaw agents add work

# 配置工作 Agent 的 API
openclaw agents set-identity work

# 切换到工作 Agent 的会话
openclaw sessions --agent work
```

### Q: 定时任务不执行怎么办？

**A:**
```bash
# 1. 检查调度器状态
openclaw cron status

# 2. 检查任务是否启用
openclaw cron list

# 3. 手动运行测试
openclaw cron run <job-id>

# 4. 查看运行历史
openclaw cron runs <job-id>
```

### Q: 如何备份配置？

**A:**
```bash
# 创建备份
openclaw backup create

# 验证备份
openclaw backup verify

# 备份位置：~/.openclaw/backups
```

### Q: 如何完全重置？

**A:**
```bash
# 软重置（保留配置）
openclaw reset

# 硬重置（删除所有数据）
openclaw uninstall
# 然后重新运行 openclaw configure
```

---

## 📊 命令速查表

### 日常操作

| 场景 | 命令 |
|------|------|
| 启动服务 | `openclaw gateway start` |
| 打开面板 | `openclaw dashboard` |
| 查看状态 | `openclaw gateway status` |
| 更新系统 | `openclaw update` |
| 诊断问题 | `openclaw doctor` |

### 配置管理

| 场景 | 命令 |
|------|------|
| 配置向导 | `openclaw configure` |
| 添加频道 | `openclaw channels add` |
| 配置模型 | `openclaw config set agents.defaults.model.primary <model>` |
| 安装插件 | `openclaw plugins install <package>` |

### 运维操作

| 场景 | 命令 |
|------|------|
| 查看会话 | `openclaw sessions` |
| 搜索记忆 | `openclaw memory search "关键词"` |
| 管理定时任务 | `openclaw cron list` |
| 查看日志 | `openclaw logs` |

---

## 🎯 最佳实践

### 1. 服务管理
- ✅ 生产环境使用 `gateway start`（后台服务）
- ✅ 调试时使用 `gateway run --verbose`（前景 + 日志）
- ❌ 不要混用 `start` 和 `run`（可能端口冲突）

### 2. 配置管理
- ✅ 定期备份配置 `openclaw backup create`
- ✅ 使用 `--profile` 隔离测试环境
- ❌ 不要手动编辑 JSON 配置（用 `config set`）

### 3. 记忆管理
- ✅ 定期审查 `MEMORY.md`
- ✅ 使用 `memory index` 保持索引更新
- ❌ 不要在记忆文件存敏感信息

### 4. 更新策略
- ✅ 稳定版：`openclaw update --channel stable`
- ✅ 测试新功能：`openclaw update --channel beta`
- ❌ 生产环境避免 `dev` 频道

---

## 📚 更多资源

- **官方文档**：https://docs.openclaw.ai
- **GitHub**：https://github.com/openclaw/openclaw
- **社区**：https://discord.com/invite/clawd
- **技能市场**：https://clawhub.com

---

## 🤝 贡献

欢迎提交 Issue 和 PR！

---

**最后更新**：2026-03-11  
**OpenClaw 版本**：2026.3.8
