# 阿里云 OSS Python SDK V2 参考文档

## 安装

```bash
pip install alibabacloud-oss-v2
```

## 环境变量配置

本 skill 使用以下三个环境变量（**必须设置**）：

| 环境变量 | 说明 | 示例值 |
|---|---|---|
| `OSS_ACCESS_KEY_ID` | 阿里云 AccessKey ID | `LTAI5t...` |
| `OSS_ACCESS_KEY_SECRET` | 阿里云 AccessKey Secret | `abc123...` |
| `OSS_REGION` | Bucket 所在地域 | `cn-hangzhou` |
| `OSS_BUCKET` | 默认 Bucket 名称（命令行 --bucket 可覆盖） | `my-bucket` |

**常用地域 ID：**

| 地域 | Region ID |
|---|---|
| 华东1（杭州）| `cn-hangzhou` |
| 华东2（上海）| `cn-shanghai` |
| 华北1（青岛）| `cn-qingdao` |
| 华北2（北京）| `cn-beijing` |
| 华南1（深圳）| `cn-shenzhen` |
| 华西1（成都）| `cn-chengdu` |
| 海外（新加坡）| `ap-southeast-1` |
| 海外（美国西部）| `us-west-1` |

## SDK 核心用法

### 初始化客户端

```python
import alibabacloud_oss_v2 as oss

credentials_provider = oss.credentials.StaticCredentialsProvider(
    access_key_id="your-key-id",
    access_key_secret="your-key-secret",
)
cfg = oss.config.load_default()
cfg.credentials_provider = credentials_provider
cfg.region = "cn-hangzhou"

client = oss.Client(cfg)
```

### 上传文件（PutObject）

```python
with open("local-file.txt", "rb") as f:
    result = client.put_object(oss.PutObjectRequest(
        bucket="my-bucket",
        key="path/to/object.txt",
        body=f,
    ))
# result.etag, result.status_code
```

### 下载文件（GetObject）

```python
result = client.get_object(oss.GetObjectRequest(
    bucket="my-bucket",
    key="path/to/object.txt",
))
with open("downloaded.txt", "wb") as f:
    f.write(result.body.read())
```

### 删除文件（DeleteObject）

```python
client.delete_object(oss.DeleteObjectRequest(
    bucket="my-bucket",
    key="path/to/object.txt",
))
```

### 列举文件（ListObjectsV2，支持分页）

```python
paginator = client.list_objects_v2_paginator()
for page in paginator.iter_page(oss.ListObjectsV2Request(
    bucket="my-bucket",
    prefix="docs/",    # 可选，按前缀过滤
)):
    for obj in (page.contents or []):
        print(obj.key, obj.size, obj.last_modified)
```

### 复制文件（CopyObject）

```python
result = client.copy_object(oss.CopyObjectRequest(
    bucket="dst-bucket",
    key="new/path.txt",
    source_bucket="src-bucket",
    source_key="old/path.txt",
))
# result.etag
```

### 生成预签名下载 URL（Presign）

```python
import datetime

expire_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=3600)

result = client.presign(oss.PresignRequest(
    method="GET",
    bucket="my-bucket",
    key="path/to/object.txt",
    expiration=expire_at,  # datetime 对象，UTC 时区
))
print(result.url)  # 带签名的临时下载 URL
```

**预签名 URL 有效期限制：** 最长 604800 秒（7 天）

## oss_client.py 脚本用法

`scripts/oss_client.py` 是本 skill 提供的命令行工具，支持所有 CRUD 操作。

### 子命令速览

```bash
# 上传（Bucket 从 OSS_BUCKET 读取，也可用 --bucket 覆盖）
python oss_client.py upload --file <local_path> [--key <oss_key>] [--bucket <bucket>]

# 下载
python oss_client.py download --key <oss_key> [--output <local_path>] [--bucket <bucket>]

# 删除
python oss_client.py delete --key <oss_key> [--bucket <bucket>]

# 列举（前缀过滤、数量限制）
python oss_client.py list [--prefix <prefix>] [--max <n>] [--bucket <bucket>]

# 复制（跨 Bucket 也支持）
python oss_client.py copy --src-key <old_key> --dst-key <new_key> [--bucket <bucket>]

# 重命名 = 复制 + 删除源
python oss_client.py copy --src-key <old_key> --dst-key <new_key> --delete-source

# 生成预签名 URL（默认 1 小时，最长 7 天）
python oss_client.py presign --key <oss_key> --expires <seconds> [--bucket <bucket>]
```

## 常见错误排查

| 错误 | 原因 | 解决方案 |
|---|---|---|
| `NoSuchBucket` | Bucket 不存在或 Region 错误 | 检查 Bucket 名称和 `OSS_REGION` |
| `InvalidAccessKeyId` | AccessKey ID 错误 | 检查 `OSS_ACCESS_KEY_ID` |
| `SignatureDoesNotMatch` | AccessKey Secret 错误 | 检查 `OSS_ACCESS_KEY_SECRET` |
| `AccessDenied` | 权限不足 | 检查 RAM 用户的 OSS 权限策略 |
| `NoSuchKey` | 对象不存在 | 检查 Key 路径拼写 |
| `RequestTimeTooSkewed` | 本地时钟误差过大 | 同步系统时间 |
