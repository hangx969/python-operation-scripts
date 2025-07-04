#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量文件扩展名重命名脚本

功能描述:
    本脚本用于批量修改指定目录下所有文件的扩展名。支持将旧扩展名的文件
    统一重命名为新的扩展名，实现文件类型的批量转换和标准化管理。

技术实现:
    - 使用 os.listdir() 遍历目录中的所有文件
    - 使用 str.endswith() 方法过滤指定扩展名的文件
    - 使用 os.path.splitext() 分离文件名和扩展名
    - 使用 os.path.join() 构造安全的文件路径
    - 使用 os.rename() 执行文件重命名操作
"""

import os

file_dir = './'

old_ext = '.txt'
new_ext = '.bak'

for file in os.listdir(file_dir):
    if file.endswith(old_ext):
        # 把文件名和扩展名分离成list，[0]是文件名，[1]是扩展名
        base_name = os.path.splitext(file)[0]
        new_file_path = os.path.join(file_dir, base_name + new_ext)
        old_file_path = os.path.join(file_dir, file)
        os.rename(old_file_path, new_file_path)
        print(f'Renamed {old_file_path} to {new_file_path}')
