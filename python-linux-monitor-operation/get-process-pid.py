"""
系统进程PID获取脚本

功能描述:
    该脚本用于获取系统中所有正在运行进程的PID和进程名称信息。
    使用psutil库遍历系统进程，提供简洁清晰的进程信息展示。

技术实现:
    - psutil.process_iter(): 遍历系统中所有运行的进程
    - 指定返回参数['pid', 'name']获取进程ID和名称
    - proc.info: 获取进程信息字典

"""

import psutil

# psutil.process_iter()返回一个process对象，遍历系统中所有正在运行的进程。
# ['pid', 'name']参数让其返回每个进程的PID和name。
for proc in psutil.process_iter(['pid', 'name']):
    # proc.info获取到一个字典，字典的kv是process_iter()里面我们规定的参数。类似于{'pid': 2958594, 'name': 'sh'}
    print(f"PID: {proc.info['pid']}, process name: {proc.info['name']}")