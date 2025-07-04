#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
旧日志文件自动清理脚本

功能描述:
    本脚本用于自动清理指定目录下的过期日志文件。基于文件的最后修改时间，
    删除超过保留期限的日志文件，有效管理磁盘空间，防止日志文件无限增长
    导致的存储空间耗尽问题。

技术实现:
    - 使用 os.listdir() 遍历日志目录中的所有文件
    - 使用 os.path.getmtime() 获取文件最后修改时间
    - 使用 time.time() 获取当前时间戳
    - 使用 os.remove() 安全删除过期文件
    - 时间计算基于 Unix 时间戳和秒数转换

"""

import os, time

log_dir = 'path/to/logs'

retention_days = 30
current_time = time.time()
cutoff = current_time - (retention_days * 86400)

for file in os.listdir(log_dir):
    # 获取绝对路径
    file_path = os.path.join(log_dir, file)

    # 检查是否是文件
    if os.path.isfile(file_path):
        file_mtime = os.path.getmtime(file_path)

        # 如果文件的修改时间早于保留截止时间，则删除
        if file_mtime < cutoff:
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")