# wyq-code-skills

> **wyqCode 技能中心** —— 为 [wyqCode] 打造的实用 Skill 合集，由 wyqCode 整理并对外分享。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Skills](https://img.shields.io/badge/Skills-2-blue)](#skill-列表)
[![Language](https://img.shields.io/badge/Language-Python-3776AB?logo=python&logoColor=white)](https://www.python.org)

---

## 什么是 Skill？

Skill 是 向 AI 注入专业知识、标准工作流和可执行脚本，让 AI 助手拥有更强的垂直能力。只需一键安装，即可在对话中直接调用。

---

## Skill 列表

| Skill | 描述 | 语言 |
|-------|------|------|
| [aliyun-oss](#-aliyun-oss) | 阿里云 OSS 文件增删改查 + 预签名 URL 生成 | Python |
| [java-alibaba-developer](#-java-alibaba-developer) | 阿里巴巴 Java 开发规范（泰山版）指导 | — |

---

## 📦 aliyun-oss

基于阿里云官方 Python SDK（`alibabacloud-oss-v2` V2）实现的完整 OSS 文件操作 Skill。

### 功能

| 操作 | 说明 |
|------|------|
| 📤 `upload` | 上传本地文件到 OSS |
| 📥 `download` | 从 OSS 下载文件到本地 |
| 🗑️ `delete` | 删除 OSS 对象 |
| 📋 `list` | 列举 Bucket 文件，支持前缀过滤 |
| 📋 `copy` | 复制 / 重命名对象（支持跨 Bucket） |
| 🔗 `presign` | 生成带过期时间的临时下载链接（最长 7 天） |

### 快速上手

**1. 设置环境变量**

```bash
export OSS_ACCESS_KEY_ID="your-access-key-id"
export OSS_ACCESS_KEY_SECRET="your-access-key-secret"
export OSS_REGION="cn-hangzhou"        # Bucket 所在地域
export OSS_BUCKET="your-bucket-name"  # 默认 Bucket
```

**2. 在 AI工具 中安装 Skill**

将 `aliyun-oss/` 目录放入 AI工具 Skill 目录。

**3. 对话触发示例**

```
帮我把 ./report.pdf 上传到 OSS 的 docs/ 目录
从 OSS 下载 docs/report.pdf 到本地
列举 OSS 中 docs/ 前缀下的所有文件
生成 docs/report.pdf 的 1 小时有效下载链接
```

### 命令行直接使用

内置 `scripts/oss_client.py` 也可脱离 AI 独立运行（SDK 缺失时自动安装）：

```bash
# 上传
python aliyun-oss/scripts/oss_client.py upload --file ./report.pdf --key docs/report.pdf

# 下载
python aliyun-oss/scripts/oss_client.py download --key docs/report.pdf --output ./report.pdf

# 删除
python aliyun-oss/scripts/oss_client.py delete --key docs/report.pdf

# 列举（前缀过滤 + 数量限制）
python aliyun-oss/scripts/oss_client.py list --prefix docs/ --max 50

# 复制 / 重命名
python aliyun-oss/scripts/oss_client.py copy --src-key old.txt --dst-key new.txt --delete-source

# 生成预签名 URL（3600 秒 = 1 小时）
python aliyun-oss/scripts/oss_client.py presign --key docs/report.pdf --expires 3600
```

---

## ☕ java-alibaba-developer

基于**阿里巴巴 Java 开发手册（泰山版）**构建的 AI 编程规范指导 Skill，让 AI 在生成 Java 代码时自动遵循阿里规范。

### 覆盖范围

- **命名规范** — 包、类、方法、变量、常量的标准命名规则
- **代码结构** — 文件布局、导入组织、方法长度
- **异常处理** — 异常层次、try-catch 使用规范
- **并发编程** — 线程安全、锁、线程池、volatile 与原子类
- **日志规范** — 日志级别、结构化日志、敏感信息保护
- **数据库操作** — SQL 规范、事务管理、ORM 最佳实践
- **API 设计** — RESTful 规范、DTO、分页、版本控制、输入验证
- **性能优化** — 字符串处理、集合使用、缓存策略
- **安全考虑** — 输入验证、输出编码、认证授权、敏感数据保护

### 适用场景

在对话中描述 Java 开发需求，AI 将自动参照阿里规范生成代码，适合：

- Spring Boot / Spring Cloud 项目开发
- 代码 Review 与质量检查
- 团队规范统一与新人培训

---

## 目录结构

```
wyq-code-skills/
├── aliyun-oss/
│   ├── SKILL.md            # Skill 主文档（AI 读取）
│   ├── scripts/
│   │   └── oss_client.py   # OSS 命令行工具
│   ├── references/
│   │   └── api_reference.md
│   └── assets/
├── java-alibaba-developer/
│   ├── SKILL.md            # Java 规范 Skill 文档
│   ├── scripts/
│   ├── references/
│   └── assets/
└── LICENSE
```

---

## 贡献 / Contributing

欢迎提交 Issue 或 PR！如果你也有好用的 Skill 想加入合集，请参考现有 Skill 结构提交。

---

## 许可证

[MIT License](./LICENSE) © wyqCode
