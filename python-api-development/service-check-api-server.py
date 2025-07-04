#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
服务管理 REST API 服务器

功能描述:
    本脚本提供基于 Flask 框架的 RESTful API 服务，用于远程管理和控制系统服务。
    主要针对 Nginx 服务提供状态查询和重启操作，支持 API Key 认证机制，
    实现安全的远程服务管理功能。

技术实现:
    - 使用 Flask 框架构建 Web API 服务
    - 使用 subprocess 模块执行系统管理命令
    - 采用 systemctl 命令管理 systemd 服务
    - 实现 HTTP 请求头认证机制
    - 支持标准 HTTP 状态码响应

API 接口设计:
    1. 服务状态查询接口:
       - 路径: GET /api/service/status
       - 功能: 查询 Nginx 服务当前运行状态
       - 认证: 无需认证
       - 响应: JSON 格式的状态信息

    2. 服务重启接口:
       - 路径: POST /api/service/restart
       - 功能: 重启 Nginx 服务
       - 认证: 需要 Bearer Token 认证
       - 响应: JSON 格式的操作结果

API 调用示例:
    状态查询:
    curl -X GET http://localhost:5000/api/service/status

    服务重启:
    curl -X POST http://localhost:5000/api/service/restart \
         -H "Authorization: Bearer YOUR_API_KEY"
"""

from flask import Flask, jsonify, request
import subprocess

app = Flask(__name__)

# 检查nginx服务状态
# # 返回running说明服务正在运行，返回stopped说明服务已停止
def check_status():
    try:
        # 通过systemctl检查状态
        result = subprocess.run(['systemctl', 'is-active', 'nginx'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)
        return 'running' if (result.returncode == 0 and result.stdout.strip() == 'active') else 'stopped'
    except Exception as e:
        return f"Error: {str(e)}."

# 重启nginx
# 返回restarted说明已经重启
# 返回其他说明产生报错
def restart_service():
    try:
        result = subprocess.run(
            ['systemctl', 'restart', 'nginx'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return 'restarted' if result.returncode == 0 else f"Failed to restart: {result.returncode}."
    except Exception as e:
        # 在函数里面的try...except，要用return来返回
        return f'Error: {str(e)}'

# flask定义服务状态查询接口
@app.route('/api/service/status', methods=['GET'])
def service_status_api():
    status = check_status()
    # 定义http请求的返回
    return jsonify({'status': status})

# flask定义重启服务接口
@app.route('/api/service/restart', methods=['POST'])
def restart_service_api():
    # 先检查api key认证
    if request.headers.get('Authorization') == 'Bearer YOUR_API_KEY':
        # 执行重启操作获取返回结果
        result = restart_service()
        if result == 'restarted':
            # flask的路由返回值可以在第二个参数显式设定status_code
            return jsonify({'message': 'Service restarted successfully'}), 200
        else:
            return jsonify({'error': f'Unexpected result: {result}'}), 500
    # 认证不通过返回401
    else:
        return jsonify({'error': 'Unauthorized'}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)