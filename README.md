# AI Daily Collection

每天自动收集全网 AI 热点和 GitHub 热门开源项目，并推送到 Notion。

## 功能特性

- 🕒 **自动定时执行**：每天 10:00 AM（香港时间）自动运行
- 🤖 **AI 热点收集**：从 Hacker News 获取最新的 AI 相关帖子
- ⭐ **GitHub 热门项目**：搜索和收集热门 AI/机器学习开源项目
- 📝 **自动推送到 Notion**：创建格式化的日报页面
- 🌐 **云端运行**：使用 GitHub Actions，不需要本地电脑开机

## 技术栈

- **Python 3.13**：主要脚本语言
- **GitHub Actions**：自动化工作流
- **Notion API**：数据存储
- **Hacker News API**：AI 热点来源
- **GitHub Search API**：热门项目来源

## 安装和配置

### 前置要求

1. **GitHub 账户**：需要一个 GitHub 账户
2. **Notion Integration**：
   - 访问 https://www.notion.so/my-integrations
   - 创建新的 integration（名称任意，例如 "AI Daily Bot"）
   - 复制 API 密钥（以 `ntn_` 或 `secret_` 开头）
3. **Notion 数据库**：
   - 在 Notion 中创建一个数据库或页面
   - 获取其 ID（32位字母数字）

### 配置步骤

1. **复制此仓库**
   ```bash
   git clone https://github.com/284456879/ai-daily-v2.git
   cd ai-daily-v2
   ```

2. **设置 GitHub Secrets**
   
   在仓库页面点击 `Settings` → `Secrets and variables` → `Actions`，添加以下两个 secrets：

   - **NOTION_KEY**: 您的 Notion API 密钥
   - **NOTION_DATABASE_ID**: 您的 Notion 数据库/页面 ID

3. **手动测试运行**
   ```bash
   gh workflow run "AI Daily Collection"
   ```

## 使用说明

### 自动执行

- **运行时间**：每天 10:00 AM（香港时间，UTC 02:00）
- **首次运行**：会在设置后的第二天开始
- **查看日志**：访问仓库的 `Actions` 标签页

### 手动执行

如果需要立即运行收集脚本：

```bash
# 使用 GitHub CLI
gh workflow run "AI Daily Collection"

# 或者在本地运行
python collect_ai_daily.py
```

注意：本地运行需要先设置环境变量：
```bash
export NOTION_KEY="your_notion_key"
export NOTION_DATABASE_ID="your_database_id"
python collect_ai_daily.py
```

## 输出示例

### AI 热点示例

- "How does AI impact skill formation?" - Hacker News - 120 points
- "OpenAI releases new GPT-4 model" - Hacker News - 85 points
- "AI in healthcare: opportunities and challenges" - Product Hunt - Daily AI Products

### GitHub 热门项目示例

- tensorflow (Python) - 182,342 stars - An end-to-end open source machine learning platform
- pytorch (Python) - 73,821 stars - Tensors and Dynamic Neural Networks in Python
- stable-diffusion (Python) - 131,456 stars - A latent text-to-image diffusion model
- langchain (Python) - 85,234 stars - Building applications with LLMs through composability

## 工作原理

### 1. AI 热点收集

从 **Hacker News** 获取最新的故事，然后使用关键词过滤 AI 相关内容：
- AI, artificial intelligence, machine learning, deep learning
- neural, LLM, GPT, Claude, openai, chatgpt

### 2. GitHub 热门项目收集

使用 **GitHub Search API** 搜索热门 AI 相关仓库：
- 搜索多个查询以获得多样化的结果
- 按星标数排序
- 自动去重
- 每个查询取前 3 个结果，总共最多 15 个项目

### 3. Notion 推送

使用 **Notion API (2025-09-03)** 创建页面：
- 标题：`AI Daily {date}`
- 内容：结构化的 AI 热点和 GitHub 项目列表
- 自动格式化和链接

## 故障排除

### 问题：GitHub Actions 失败

**解决方案：**
1. 检查 Secrets 是否正确配置
   - `Settings` → `Secrets and variables` → `Actions`
   - 确认 `NOTION_KEY` 和 `NOTION_DATABASE_ID` 已设置

2. 查看 Actions 日志
   - 访问 `Actions` 标签页
   - 点击失败的运行查看详细错误信息

3. 验证 Notion API 密钥
   - 确保密钥有正确的权限
   - 确认数据库/页面已分享给 integration

### 问题：Notion 页面创建失败

**解决方案：**
1. 检查 `NOTION_DATABASE_ID` 是否正确
   - 从 Notion 页面 URL 复制（32位字母数字）
   - 确保没有多余的破折号

2. 确认 integration 已连接
   - 在 Notion 页面右上角点击 `...`
   - 选择 `Add connections`
   - 选择您的 integration

### 问题：GitHub API 速率限制

**说明：**
- GitHub 公开 API 有速率限制（约 60 次/小时）
- 如果达到限制，脚本会自动处理

**解决方案：**
- 脚本会捕获错误并继续运行
- 可以减少搜索查询数量

## 项目结构

```
ai-daily-v2/
├── .github/
│   └── workflows/
│       └── ai-daily.yml      # GitHub Actions 工作流
├── collect_ai_daily.py           # 主要 Python 脚本
├── requirements.txt              # Python 依赖
└── README.md                    # 此文件
```

## Python 脚本说明

### collect_ai_daily.py

主要模块：

- `collect_ai_hotspots()`: 收集 AI 热点
- `collect_github_trending()`: 收集 GitHub 热门项目
- `create_notion_page()`: 创建 Notion 页面
- `main()`: 主函数，协调整个模块

### 环境变量

- `NOTION_KEY`: Notion API 密钥
- `NOTION_DATABASE_ID`: Notion 数据库/页面 ID

## 依赖

```
requests>=2.31.0
pytz>=2023.3
```

## 许可证

MIT License - 自由使用和修改

## 贡献

欢迎贡献！您可以：

1. Fork 此仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 作者

由 [284456879](https://github.com/284456879) 创建和维护

## 致谢

- **GitHub Actions**：提供自动化平台
- **Notion**：提供优秀的 API 和数据库服务
- **Hacker News**：AI 热点来源
- **GitHub**：开源项目平台

## 许可

MIT

---

**注意**：此项目仅用于学习和个人用途。使用时请遵守相关服务的使用条款。
