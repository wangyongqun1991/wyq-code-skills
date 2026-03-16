#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿里云 OSS 文件操作工具
支持：上传、下载、删除、列举、复制（重命名）、生成预签名下载链接
凭证从环境变量读取：
  - OSS_ACCESS_KEY_ID
  - OSS_ACCESS_KEY_SECRET
  - OSS_REGION
  - OSS_BUCKET       默认 Bucket（命令行 --bucket 可覆盖）
"""

import argparse
import os
import sys
import datetime

# ---------------------------------------------------------------------------
# 依赖检查
# ---------------------------------------------------------------------------

def _ensure_sdk():
    try:
        import alibabacloud_oss_v2 as oss  # noqa: F401
    except ImportError:
        print("[INFO] 未检测到 alibabacloud-oss-v2，正在自动安装...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "alibabacloud-oss-v2", "-q"])
        print("[INFO] 安装完成")

_ensure_sdk()

import alibabacloud_oss_v2 as oss  # noqa: E402

# ---------------------------------------------------------------------------
# 客户端构建
# ---------------------------------------------------------------------------

def build_client():
    """从环境变量构建 OSS 客户端，同时返回默认 Bucket 名称"""
    access_key_id = os.environ.get("OSS_ACCESS_KEY_ID", "").strip()
    access_key_secret = os.environ.get("OSS_ACCESS_KEY_SECRET", "").strip()
    region = os.environ.get("OSS_REGION", "").strip()
    default_bucket = os.environ.get("OSS_BUCKET", "").strip()

    missing = []
    if not access_key_id:
        missing.append("OSS_ACCESS_KEY_ID")
    if not access_key_secret:
        missing.append("OSS_ACCESS_KEY_SECRET")
    if not region:
        missing.append("OSS_REGION")
    if not default_bucket:
        missing.append("OSS_BUCKET")

    if missing:
        print(f"[ERROR] 缺少必要环境变量: {', '.join(missing)}")
        print("请设置以下环境变量后重试：")
        print("  export OSS_ACCESS_KEY_ID=<your-access-key-id>")
        print("  export OSS_ACCESS_KEY_SECRET=<your-access-key-secret>")
        print("  export OSS_REGION=<region-id>      # 例如: cn-hangzhou")
        print("  export OSS_BUCKET=<bucket-name>    # 默认 Bucket 名称")
        sys.exit(1)

    credentials_provider = oss.credentials.StaticCredentialsProvider(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
    )
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = region
    return oss.Client(cfg), default_bucket


# ---------------------------------------------------------------------------
# 各操作函数
# ---------------------------------------------------------------------------

def cmd_upload(args):
    """上传本地文件到 OSS"""
    client, default_bucket = build_client()
    bucket = args.bucket or default_bucket
    key = args.key or os.path.basename(args.file)
    local_file = args.file

    if not os.path.exists(local_file):
        print(f"[ERROR] 本地文件不存在: {local_file}")
        sys.exit(1)

    print(f"[INFO] 上传 {local_file} → oss://{bucket}/{key}")
    with open(local_file, "rb") as f:
        result = client.put_object(oss.PutObjectRequest(
            bucket=bucket,
            key=key,
            body=f,
        ))
    print(f"[OK] 上传成功")
    print(f"     ETag       : {result.etag}")
    print(f"     StatusCode : {result.status_code}")


def cmd_download(args):
    """从 OSS 下载文件到本地"""
    client, default_bucket = build_client()
    bucket = args.bucket or default_bucket
    key = args.key
    local_file = args.output or os.path.basename(key)

    print(f"[INFO] 下载 oss://{bucket}/{key} → {local_file}")
    result = client.get_object(oss.GetObjectRequest(
        bucket=bucket,
        key=key,
    ))
    os.makedirs(os.path.dirname(os.path.abspath(local_file)), exist_ok=True)
    with open(local_file, "wb") as f:
        f.write(result.body.read())
    print(f"[OK] 下载成功 → {local_file}")
    print(f"     ContentType: {result.content_type}")
    print(f"     ContentLen : {result.content_length}")


def cmd_delete(args):
    """删除 OSS 上的文件"""
    client, default_bucket = build_client()
    bucket = args.bucket or default_bucket
    key = args.key

    print(f"[INFO] 删除 oss://{bucket}/{key}")
    client.delete_object(oss.DeleteObjectRequest(
        bucket=bucket,
        key=key,
    ))
    print(f"[OK] 已删除 oss://{bucket}/{key}")


def cmd_list(args):
    """列举 OSS Bucket 中的文件"""
    client, default_bucket = build_client()
    bucket = args.bucket or default_bucket
    prefix = args.prefix or ""
    max_count = args.max or 100

    print(f"[INFO] 列举 oss://{bucket}/{prefix}* (最多 {max_count} 条)")
    paginator = client.list_objects_v2_paginator()

    count = 0
    for page in paginator.iter_page(oss.ListObjectsV2Request(
        bucket=bucket,
        prefix=prefix if prefix else None,
    )):
        for obj in (page.contents or []):
            size_kb = (obj.size or 0) / 1024
            print(f"  {obj.key:<60} {size_kb:>8.2f} KB  {obj.last_modified}")
            count += 1
            if count >= max_count:
                print(f"[INFO] 已达最大显示数量 {max_count}，停止列举")
                return

    if count == 0:
        print("[INFO] 未找到任何对象")
    else:
        print(f"[OK] 共列举 {count} 个对象")


def cmd_copy(args):
    """在 OSS 内复制文件（可用于重命名：复制后删除源）"""
    client, default_bucket = build_client()
    src_bucket = args.src_bucket or args.bucket or default_bucket
    src_key = args.src_key
    dst_bucket = args.dst_bucket or args.bucket or default_bucket
    dst_key = args.dst_key

    print(f"[INFO] 复制 oss://{src_bucket}/{src_key} → oss://{dst_bucket}/{dst_key}")
    result = client.copy_object(oss.CopyObjectRequest(
        bucket=dst_bucket,
        key=dst_key,
        source_bucket=src_bucket,
        source_key=src_key,
    ))
    print(f"[OK] 复制成功")
    print(f"     ETag: {result.etag}")

    if args.delete_source:
        print(f"[INFO] 删除源文件 oss://{src_bucket}/{src_key}")
        client.delete_object(oss.DeleteObjectRequest(
            bucket=src_bucket,
            key=src_key,
        ))
        print(f"[OK] 源文件已删除（重命名完成）")


def cmd_presign(args):
    """生成带过期时间的预签名下载 URL"""
    client, default_bucket = build_client()
    bucket = args.bucket or default_bucket
    key = args.key
    expires = args.expires  # 秒

    expire_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=expires)

    print(f"[INFO] 生成预签名 URL: oss://{bucket}/{key}，有效期 {expires} 秒")

    result = client.presign(oss.PresignRequest(
        method="GET",
        bucket=bucket,
        key=key,
        expiration=expire_at,
    ))

    print(f"[OK] 预签名 URL 生成成功")
    print(f"     URL       : {result.url}")
    print(f"     过期时间   : {expire_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"     有效期     : {expires} 秒")


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="阿里云 OSS 文件操作工具 (alibabacloud-oss-v2)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
环境变量（必须设置）:
  OSS_ACCESS_KEY_ID      阿里云 AccessKey ID
  OSS_ACCESS_KEY_SECRET  阿里云 AccessKey Secret
  OSS_REGION             Bucket 所在地域，例如 cn-hangzhou
  OSS_BUCKET             默认 Bucket 名称（命令行 --bucket 可覆盖）

子命令示例:
  # 上传文件（使用环境变量中的默认 Bucket）
  python oss_client.py upload --file ./report.pdf --key docs/report.pdf

  # 上传文件（覆盖为指定 Bucket）
  python oss_client.py upload --bucket other-bucket --file ./report.pdf --key docs/report.pdf

  # 下载文件
  python oss_client.py download --key docs/report.pdf --output ./report.pdf

  # 删除文件
  python oss_client.py delete --key docs/report.pdf

  # 列举文件（可指定前缀）
  python oss_client.py list --prefix docs/ --max 50

  # 复制文件（跨 Bucket 也支持）
  python oss_client.py copy --src-key old/path.txt --dst-key new/path.txt

  # 重命名（复制 + 删除源）
  python oss_client.py copy --src-key old.txt --dst-key new.txt --delete-source

  # 生成 1 小时有效的预签名下载链接
  python oss_client.py presign --key docs/report.pdf --expires 3600
        """
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- upload ---
    p_upload = subparsers.add_parser("upload", help="上传本地文件到 OSS")
    p_upload.add_argument("--bucket", default=None, help="目标 Bucket 名称（默认读取 OSS_BUCKET 环境变量）")
    p_upload.add_argument("--file", required=True, help="本地文件路径")
    p_upload.add_argument("--key", help="OSS 对象 Key（默认使用文件名）")
    p_upload.set_defaults(func=cmd_upload)

    # --- download ---
    p_download = subparsers.add_parser("download", help="从 OSS 下载文件")
    p_download.add_argument("--bucket", default=None, help="Bucket 名称（默认读取 OSS_BUCKET 环境变量）")
    p_download.add_argument("--key", required=True, help="OSS 对象 Key")
    p_download.add_argument("--output", help="本地保存路径（默认使用 Key 文件名部分）")
    p_download.set_defaults(func=cmd_download)

    # --- delete ---
    p_delete = subparsers.add_parser("delete", help="删除 OSS 上的文件")
    p_delete.add_argument("--bucket", default=None, help="Bucket 名称（默认读取 OSS_BUCKET 环境变量）")
    p_delete.add_argument("--key", required=True, help="OSS 对象 Key")
    p_delete.set_defaults(func=cmd_delete)

    # --- list ---
    p_list = subparsers.add_parser("list", help="列举 OSS Bucket 中的文件")
    p_list.add_argument("--bucket", default=None, help="Bucket 名称（默认读取 OSS_BUCKET 环境变量）")
    p_list.add_argument("--prefix", default="", help="对象前缀过滤（可选）")
    p_list.add_argument("--max", type=int, default=100, help="最多显示条数（默认 100）")
    p_list.set_defaults(func=cmd_list)

    # --- copy ---
    p_copy = subparsers.add_parser("copy", help="在 OSS 内复制或重命名文件")
    p_copy.add_argument("--bucket", default=None, help="默认 Bucket（源和目标共用，默认读取 OSS_BUCKET 环境变量）")
    p_copy.add_argument("--src-bucket", dest="src_bucket", help="源 Bucket（不填则使用 --bucket 或 OSS_BUCKET）")
    p_copy.add_argument("--src-key", dest="src_key", required=True, help="源对象 Key")
    p_copy.add_argument("--dst-bucket", dest="dst_bucket", help="目标 Bucket（不填则使用 --bucket 或 OSS_BUCKET）")
    p_copy.add_argument("--dst-key", dest="dst_key", required=True, help="目标对象 Key")
    p_copy.add_argument("--delete-source", dest="delete_source", action="store_true",
                        help="复制后删除源文件（实现重命名）")
    p_copy.set_defaults(func=cmd_copy)

    # --- presign ---
    p_presign = subparsers.add_parser("presign", help="生成带过期时间的预签名下载 URL")
    p_presign.add_argument("--bucket", default=None, help="Bucket 名称（默认读取 OSS_BUCKET 环境变量）")
    p_presign.add_argument("--key", required=True, help="OSS 对象 Key")
    p_presign.add_argument("--expires", type=int, default=3600,
                           help="URL 有效期（秒），默认 3600（1 小时），最长 604800（7 天）")
    p_presign.set_defaults(func=cmd_presign)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
