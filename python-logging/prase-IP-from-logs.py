#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志文件 IP 地址提取脚本

功能描述:
    本脚本用于从日志文件中提取所有的 IPv4 地址。通过正则表达式匹配标准的 IP 地址格式，
    快速识别和提取日志中的 IP 信息，支持各种日志格式的 IP 地址解析。

技术实现:
    - 使用 re 模块进行正则表达式匹配
    - 采用预编译正则表达式提高匹配效率
    - 使用 findall() 方法获取所有匹配结果
    - 文件读取采用上下文管理器确保资源释放

正则表达式详解:
    模式: r'\\b(?:[0-9]{1,3}\\.){3}[0-9]{1,3}\\b'
    - \\b: 单词边界，确保匹配完整的 IP 地址
    - (?:[0-9]{1,3}): 非捕获组，匹配1-3位数字
    - \\.: 匹配点号分隔符
    - {3}: 重复3次，匹配前三个数字段
    - [0-9]{1,3}: 匹配最后一个数字段

IP 地址格式:
    IPv4 地址标准格式: XXX.XXX.XXX.XXX
    - 每个数字段范围: 0-255
    - 分隔符: 点号 (.)
    - 总长度: 7-15 个字符
"""

import re
log_file = './example.txt'
#读取日志文件
with open(log_file, 'r') as f:
    logs = f.read()
    ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    ips = ip_pattern.findall(logs)
    for ip in ips:
        print(ip)