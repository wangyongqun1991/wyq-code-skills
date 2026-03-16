---
name: aliyun-oss
description: "This skill should be used when users need to perform file operations on Alibaba Cloud OSS (Object Storage Service), including uploading files, downloading files, deleting files, listing objects, copying/renaming files, and generating presigned download URLs with expiration time. Trigger phrases include OSS upload, OSS download, OSS delete, OSS list files, OSS presigned URL, Alibaba Cloud OSS file management, upload to OSS, download from OSS, generate OSS presigned URL, or any request involving Alibaba Cloud OSS file management operations."
---

# 阿里云 OSS 文件操作 Skill

## 功能概述

本 skill 提供完整的阿里云 OSS 文件增删改查能力及预签名下载 URL 生成，基于官方 `alibabacloud-oss-v2` Python SDK（V2）实现。

**支持的操作：**
- 📤 **上传**（upload）：将本地文件上传到 OSS
- 📥 **下载**（download）：从 OSS 下载文件到本地
- 🗑️ **删除**（delete）：删除 OSS 上的对象
- 📋 **列举**（list）：列举 Bucket 中的文件，支持前缀过滤
- 📋 **复制/重命名**（copy）：在 OSS 内复制对象，可选删除源实现重命名
- 🔗 **预签名 URL**（presign）：生成带过期时间的临时下载链接

## 环境变量要求

执行任何操作前，必须确认用户已设置以下四个环境变量：

| 环境变量 | 说明 |
|---|---|
| `OSS_ACCESS_KEY_ID` | 阿里云 AccessKey ID |
| `OSS_ACCESS_KEY_SECRET` | 阿里云 AccessKey Secret |
| `OSS_REGION` | Bucket 所在地域（如 `cn-hangzhou`） |
| `OSS_BUCKET` | 默认 Bucket 名称（命令行 `--bucket` 可覆盖） |

若用户未设置，提示用户执行：
```bash
export OSS_ACCESS_KEY_ID="your-key-id"
export OSS_ACCESS_KEY_SECRET="your-key-secret"
export OSS_REGION="cn-hangzhou"
export OSS_BUCKET="your-bucket-name"
```

## 使用脚本执行操作

本 skill 内置了 `scripts/oss_client.py`，所有操作均通过该脚本执行。SDK 缺失时脚本会自动安装。

### 调用方式

直接运行脚本子命令即可完成操作。详细用法参见 `references/api_reference.md`。

```bash
# 上传文件（Bucket 从 OSS_BUCKET 读取，可用 --bucket 覆盖）
python ~/.codebuddy/skills/aliyun-oss/scripts/oss_client.py upload \
  --file <本地路径> [--key <OSS对象Key>] [--bucket <bucket名称>]

# 下载文件
python ~/.codebuddy/skills/aliyun-oss/scripts/oss_client.py download \
  --key <OSS对象Key> [--output <本地路径>] [--bucket <bucket名称>]

# 删除文件
python ~/.codebuddy/skills/aliyun-oss/scripts/oss_client.py delete \
  --key <OSS对象Key> [--bucket <bucket名称>]

# 列举文件（支持前缀过滤）
python ~/.codebuddy/skills/aliyun-oss/scripts/oss_client.py list \
  [--prefix <前缀>] [--max <最大数量>] [--bucket <bucket名称>]

# 复制文件（支持跨 Bucket）
python ~/.codebuddy/skills/aliyun-oss/scripts/oss_client.py copy \
  --src-key <源Key> --dst-key <目标Key> [--bucket <bucket名称>]

# 重命名（复制 + 删除源）
python ~/.codebuddy/skills/aliyun-oss/scripts/oss_client.py copy \
  --src-key <旧Key> --dst-key <新Key> --delete-source

# 生成预签名下载 URL（expires 单位为秒，最长 604800 即 7 天）
python ~/.codebuddy/skills/aliyun-oss/scripts/oss_client.py presign \
  --key <OSS对象Key> --expires <秒数> [--bucket <bucket名称>]
```

## 工作流程

1. **确认环境变量**：检查 `OSS_ACCESS_KEY_ID`、`OSS_ACCESS_KEY_SECRET`、`OSS_REGION`、`OSS_BUCKET` 是否已设置
2. **确认操作参数**：向用户明确 Bucket 名称、文件路径（Key）、本地路径等信息
3. **执行脚本**：调用 `scripts/oss_client.py` 对应子命令
4. **反馈结果**：将脚本输出的状态信息（ETag、URL、文件列表等）清晰展示给用户

## 参考资料

- 详细 API 用法、地域列表、错误排查：`references/api_reference.md`
- 官方 SDK 仓库：https://github.com/aliyun/alibabacloud-oss-python-sdk-v2
