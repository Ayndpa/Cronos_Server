# Cronos Server

Cronos Server 是一个基于 Python 的项目，旨在提供 RSS 服务和相关功能。

## 安装与运行

### 环境要求

- Python 3.12 或更高版本
- Node.js（如果需要运行 RSSHub）

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行项目

```bash
python run.py
```

## 功能模块

### 1. 数据模型
`models/` 目录包含项目的数据模型定义。

### 2. 路由
`routes/` 目录定义了项目的 API 路由。

### 3. RSSHub
`RSSHub/` 目录包含 RSSHub 的相关代码，用于生成 RSS 源。

### 4. 服务层
`services/` 目录实现了业务逻辑。

### 5. 数据库
`sql/` 目录存储了数据库相关的 SQL 文件。

## 开发指南

### 配置文件

请根据需要修改 `.vscode/tasks.json` 和其他配置文件。

### 数据库

项目使用 SQLite 数据库，默认数据库文件为 `cronos.db`。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进本项目。