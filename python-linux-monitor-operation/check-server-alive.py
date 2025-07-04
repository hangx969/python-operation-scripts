#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
服务器存活状态监控脚本

功能描述:
    本脚本用于持续监控多个服务器的网络连通性和存活状态。通过定期发送 ping 命令
    检测服务器的可达性，提供 24x7 的网络监控服务，及时发现网络故障和服务器宕机问题。

技术实现:
    - 使用 subprocess.run() 执行系统 ping 命令
    - 采用 while True 循环实现持续监控
    - 使用 time.sleep() 控制检测间隔
    - 通过返回码判断 ping 命令执行结果
    - 捕获标准输出和标准错误流

"""

import time
# 可以执行ping, ls等操作
import subprocess

servers = ["192.168.1.1","192.168.1.2","192.168.1.3"]
while True:
    for server in servers:
        result = subprocess.run(["ping", "-c", "1", server], capture_output=True, text=True)
        print(f"Checking {server}...")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        print(f"returncode: {result.returncode}")

        if result.returncode == 0:
            print(f"{server} is reachable.")
        else:
            print(f"{server} is not reachable.")
    time.sleep(86400)  # 等待86400秒，即24小时
    print("Waiting for the next check...\n")