"""
多核CPU使用率监控脚本

功能描述:
    该脚本用于实时监控多核处理器系统中每个CPU核心的使用率以及
    系统整体CPU使用率。提供详细的CPU性能监控数据，帮助系统管理员
    了解CPU负载分布和系统性能状况。

技术实现:
    - psutil.cpu_percent(interval=1, percpu=True): 获取每核心CPU使用率
      * interval=1: 设置1秒采样间隔
      * percpu=True: 返回每个CPU核心的独立使用率
    - psutil.cpu_percent(): 获取系统整体CPU使用率
    - 返回百分比格式的使用率数据

输出信息:
    - CPU usage of every core: 每个CPU核心的使用率列表
    - Overall CPU usage: 系统整体CPU使用率百分比

"""

import psutil

def get_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
    print(f"CPU usage of every core: {cpu_usage}.")
    print(f"Overall CPU usage: {psutil.cpu_percent()}.")

if __name__ == '__main__':
    get_cpu_usage()