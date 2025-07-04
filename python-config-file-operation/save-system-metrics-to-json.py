"""
系统指标收集与JSON存储脚本

功能描述:
    该脚本用于定时收集系统性能指标（CPU使用率、内存使用情况等），
    并将这些数据以结构化的方式存储到JSON文件中。适用于系统监控、
    性能分析、历史数据记录等场景，便于后续数据分析和可视化处理。

技术实现:
    - psutil.cpu_percent(): 获取CPU使用率百分比
    - psutil.virtual_memory(): 获取内存使用详细信息
    - datetime.now(): 获取当前时间戳
    - time.sleep(): 设置采样间隔
    - json.dump(): 将数据序列化为JSON格式
    - 列表存储多次采样结果

数据结构设计:
    单次采样数据结构:
    {
        'timestamp': '07-04 14:30:25',    # 采样时间
        'cpu_usage': 25.6,               # CPU使用率(%)
        'mem_usage': {                   # 内存使用详情
            'total': 8589934592,         # 总内存(字节)
            'available': 4294967296,     # 可用内存(字节)
            'percent': 50.0,             # 使用率(%)
            'used': 4294967296,          # 已使用内存(字节)
            'free': 4294967296           # 空闲内存(字节)
        }
    }
"""

import json, psutil, time
from datetime import datetime

# 使用python收集服务器状态，序列化到json文件
# 用列表来存放字典
status_data = []

# 连续收集五次数据
for _ in range(5):
    # 用字典来格式化收集的数据
    status ={
        'timestamp': datetime.now().strftime('%m-%d %H:%M:%S'),
        'cpu_usage': psutil.cpu_percent(),
        'mem_usage': psutil.virtual_memory()
    }
	# 把每一秒生成的数据（字典）添加到列表中
    status_data.append(status)
    time.sleep(1)

# 把列表序列化到json文件
with open('python-manuscripts/status.json', 'w') as f:
    json.dump(status_data, f, indent=4)