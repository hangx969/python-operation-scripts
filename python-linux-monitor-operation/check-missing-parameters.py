#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件参数检查脚本

功能描述:
    本脚本用于批量检查多个配置文件中是否包含指定的必需参数。
    通过正则表达式搜索配置文件内容，快速识别缺失关键配置参数的文件，
    确保系统配置的完整性和一致性。

技术实现:
    - 使用 re 模块进行正则表达式匹配
    - 采用预编译正则表达式提高搜索效率
    - 使用 search() 方法检测参数是否存在
    - 文件读取采用上下文管理器确保资源安全
"""

import re

config_files = ['config1.conf', 'config2.conf']
required_para = 'max_connections'
# 直接匹配对应的关键词
pattern = re.compile(f'{required_para}')

for file in config_files:
    with open(file, 'r') as f:
        content = f.read()
    if not pattern.search(content):
        print(f"{file} is missing required parameter \'{required_para}\'")