#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
服务器健康检查 REST API 服务

功能描述:
    本脚本提供基于 Flask 框架的 RESTful API 服务，用于实时监控和报告服务器的健康状态。
    通过 HTTP API 接口提供 CPU、内存、磁盘使用率等关键系统指标，支持外部监控系统
    和运维工具的集成，实现服务器状态的远程监控和自动化健康检查。

技术实现:
    - 使用 Flask 框架构建轻量级 Web API 服务
    - 使用 psutil 库获取系统资源使用情况
    - 采用 RESTful 设计规范定义 API 接口
    - 使用 JSON 格式进行数据序列化和传输
    - 支持 HTTP GET 方法进行状态查询

API 接口设计:
    1. 首页接口: GET /
       - 功能: 服务可用性验证
       - 响应: 简单文本消息

    2. 健康检查接口: GET /api/health
       - 功能: 获取服务器健康状态和资源使用情况
       - 响应: JSON 格式的系统指标数据

数据结构:
    健康检查响应格式:
    {
        "cpu_usage": float,     // CPU 使用率百分比
        "mem_usage": float,     // 内存使用率百分比
        "disk_usage": float,    // 磁盘使用率百分比
        "status": string        // 健康状态 ("healthy" | "unhealthy")
    }

健康状态判断逻辑:
    健康阈值设置:
    - CPU 使用率: > 80% 视为不健康
    - 内存使用率: > 80% 视为不健康
    - 磁盘使用率: > 90% 视为不健康
    - 状态判断: 任一指标超过阈值即标记为 "unhealthy"

API 调用示例:
    curl -X GET http://localhost:5000/api/health

    响应示例:
    {
        "cpu_usage": 45.2,
        "mem_usage": 67.8,
        "disk_usage": 82.1,
        "status": "healthy"
    }

"""

from flask import Flask, jsonify
import psutil

#创建flask应用
app = Flask(__name__)

@app.route('/')
def home():
    return 'This is a demo healthy check api.'

# 定义健康检查api
@app.route('/api/health',methods=['GET'])
def health_check():
    # 获取CPU使用率
    cpu_usage = psutil.cpu_percent(interval=1)
    # 获取内存使用率
    mem_usage = psutil.virtual_memory().percent
    # 获取磁盘使用情况
    disk_usage = psutil.disk_usage('/').percent
    # 判断服务器状态
    status='unhealthy' if cpu_usage > 80 or mem_usage > 80 or disk_usage > 90 else 'healthy'
    # 返回json数据
    return jsonify ({
        'cpu_usage': cpu_usage,
        'mem_usage': mem_usage,
        'disk_usage': disk_usage,
        'status': status
    })

# 启动flask服务
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)