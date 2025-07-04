#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nginx 和系统日志分析脚本

功能描述:
    本脚本提供了一个灵活的日志解析框架，支持多种日志格式的解析和分析。
    主要包含 Nginx 访问日志和系统 messages 日志的解析器，能够将非结构化的日志文本
    转换为结构化的字典数据，便于后续分析和处理。

技术实现:
    - 使用正则表达式进行复杂字符串匹配和提取
    - 采用工厂模式设计提供统一的解析器接口
    - 字符串分割和切片技术精确定位字段
    - 闭包函数实现解析器的封装和返回

数据结构:
    Nginx 日志解析结果:
    {
        'IP': '客户端IP地址',
        'date': '访问日期时间',
        'request': 'HTTP请求方法和路径',
        'status': 'HTTP状态码',
        'size': '响应体大小',
        'referer': '来源页面',
        'user_agent': '用户代理字符串'
    }

    Messages 日志解析结果:
    {
        'date': '日志日期',
        'time': '日志时间',
        'hostname': '主机名',
        'service': '服务名称',
        'message': '日志消息内容'
    }

解析器详解:
    nginx_parser:
        - 解析标准 Nginx 访问日志格式
        - 提取客户端 IP、访问时间、请求信息、状态码等
        - 处理用户代理和来源页面信息

    messages_parser:
        - 解析 Linux 系统 messages 日志格式
        - 提取日期时间、主机名、服务名称、消息内容
        - 处理服务 PID 信息的提取和清理

正则表达式说明:
    - r'(\\S+)': 匹配非空白字符，用于提取主机名
    - r'(\\S+)(?:\\[\\d+\\])': 匹配服务名并可选匹配PID部分
    - 使用捕获组提取关键信息

"""

import re

def make_log_praser(service_name):

    def nginx_praser(line):
    # IP、日期、请求方法、状态码、返回值大小、用户代理
        parts = line.split(' ')
        # ['192.168.40.80', '-', '-', '[30/Aug/2030:11:27:18', '+0800]', '"GET', '/', 'HTTP/1.1"', '200', '3429', '"-"', '"curl/7.61.1"', '"-"']

        # 直接用字符串切片获取对应的值
        return {
            'IP': parts[0],
            'date': parts[3][1:] + ' ' + parts[4][:-1],
            'request': ' '.join(parts[5:8]),
            'status': parts[8],
            'size': parts[9],
            'referer': parts[10],
            'user_agent': parts[11][1:-1]
        }


    def messages_praser(line):
        # 日期、时间、主机名、服务信息、日志消息
        #['Aug', '30', '18:08', 'myhost sshd[1234]: Accepted password for user from 192.168.1.2 port 22 ssh2']
        parts = line.split(' ', 3) # 只分割前三个空格，拿出来日期时间

        if len(parts) < 4:
            raise ValueError('Log line is too short to parse')

        date = parts[0] + ' ' + parts[1]
        time = parts[2]

        # 提取主机名部分
        rest = parts[3]
        host_part = re.match(r'(\S+)', rest) # 匹配剩余部分开头的主机名部分
        if host_part:
            hostname = host_part.group(1) # 提取正则表达式中的第一个捕获组
            rest = rest[len(hostname):].lstrip()
            # 从左边开始切片，去掉hostname部分
            # 'sshd[1234]: Accepted password for user from 192.168.1.2 port 22 ssh2'
        else:
            raise ValueError('Log line is malformed')

        # 获取 sshd 部分，去掉[1234]
        service_message_split = rest.split(':', 1) # 剩余部分用冒号分割一次，分割成两部分 ['sshd[1234]', 'Accepted......']
        if len(service_message_split) < 2:
            return ValueError('Log line is malformed')
        service_message = service_message_split[0].strip()
        # 去掉[1234]
        service_message = re.match(r'(\S+)(?:\[\d+\])', service_message)
        if service_message:
            # 匹配到就取出第1个捕获组的值
            service = service_message.group(1)
        else:
            # 没匹配到说明没有[1234]部分，service就是它本身？（有没有可能是没有前面的部分？）
            service = service_message

        # 获取 Accepted password ... 部分
        message = service_message_split[1].strip()

        # 返回字典结果
        return {
            'date': date,
            'time': time,
            'hostname': hostname,
            'service': service,
            'message': message
        }

    if service_name == 'nginx':
        return nginx_praser
    elif service_name == 'messages':
        return messages_praser
    else:
        raise ValueError('Unknown service name')

if __name__=='__main__':
    nginx_log_praser = make_log_praser('nginx')
    messages_log_praser = make_log_praser('messages')

    nginx_log = '192.168.40.80 - - [30/Aug/2030:11:27:18 +0800] "GET / HTTP/1.1" 200 3429 "-" "curl/7.61.1" "-"'
    messages_log = 'Aug 30 18:08 myhost sshd[1234]: Accepted password for user from 192.168.1.2 port 22 ssh2'

    print(nginx_log_praser(nginx_log))
    print(messages_log_praser(messages_log))