#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件和目录备份脚本

功能描述:
    本脚本用于将指定源目录下的所有文件和子目录备份到目标目录中。
    支持自动创建带时间戳的备份目录，保留文件元数据信息，实现完整的数据备份功能。
    脚本会自动处理目录结构创建、文件复制和元数据保持等操作。

技术实现:
    - 使用 os 模块进行文件系统操作和路径处理
    - 使用 shutil 模块实现高级文件复制功能
    - 使用 datetime 模块生成时间戳
    - 支持目录和文件的区分处理
"""

import os, shutil
from datetime import datetime

# 定义源目录和目标目录
src_dir = 'path/to/source/directory'
dest_dir = 'path/to/destination/directory'

# 创建源目录和目标目录，如果它们不存在
if not os.path.exists(src_dir):
    print(f"Source directory '{src_dir}' does not exist, creating it now.")
    os.makedirs(src_dir)

if not os.path.exists(dest_dir):
    print(f"Destination directory '{dest_dir}' does not exist, creating it now.")
    os.makedirs(dest_dir)

# 创建子目录，如果子目录已经存在，不抛异常
os.makedirs(os.path.join(src_dir,'subdir1'), exist_ok=True)
os.makedirs(os.path.join(src_dir,'subdir2'), exist_ok=True)

# 创建文件
with open(os.path.join(src_dir, 'file1.txt'), 'w') as f:
    f.write('This is file 1.')

with open(os.path.join(src_dir, 'file2.txt'), 'w') as f:
    f.write('This is file 2.')

# 获取时间戳，datetime.now() 返回的是从Unix epoch到现在的秒数，strftime() 方法将其格式化为字符串
timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')

# 用时间戳命名备份目录
backup_dir = os.path.join(dest_dir, f'backup_{timestamp}')
os.makedirs(backup_dir, exist_ok=True)

# 开始备份
for item in os.listdir(src_dir):
    # for循环获取到的是相对路径，所以需要使用os.path.join()来拼接源目录和目标目录
    src_item = os.path.join(src_dir, item)
    dest_item = os.path.join(backup_dir, item)

    # 判断目标是否是目录
    if os.path.isdir(src_item):
        # 复制目录。
        # dirs_exist_ok=True 目标目录如果存在不会抛异常，会覆盖掉。
        # copy_function=shutil.copy2 把源目录的metadata也复制过去
        shutil.copytree(src_item, dest_item, dirs_exist_ok=True, copy_function=shutil.copy2)
    else:
        # 复制文件，metadata也会被复制
        shutil.copy2(src_item, dest_item)

print(f"Backup completed successfully to {backup_dir}")