"""
系统综合监控报告脚本

功能描述:
    该脚本用于生成系统综合监控报告，集成了CPU使用率、内存使用率和
    磁盘空间使用情况。提供一个简洁的系统状态概览，便于快速了解
    系统当前的整体运行状况和资源使用情况。

技术实现:
    - datetime.datetime.now(): 获取当前时间并格式化
    - psutil.cpu_percent(): 获取CPU使用率百分比
    - psutil.virtual_memory().percent: 获取内存使用率百分比
    - shutil.disk_usage(): 获取指定路径的磁盘使用情况
      返回元组: (total, used, free) 以字节为单位
    - 字节到GiB的单位转换（除以2^30）

输出信息:
    - Report time: 报告生成时间（月-日格式）
    - CPU usage: CPU使用率百分比
    - Memory usage: 内存使用率百分比
    - Disk total: 磁盘总容量（GiB）
    - Disk used: 已使用磁盘空间（GiB）
    - Disk free: 剩余磁盘空间（GiB）

"""

import psutil, shutil, datetime

def get_system_report():
    report = []
    # 打印报告时间
    report.append(f"Report time: {datetime.datetime.now().strftime('%m-%d')}.")
    # 获取CPU memory使用情况
    report.append(f"CPU usage: {psutil.cpu_percent()}%.")
    report.append(f"Memory usage: {psutil.virtual_memory().percent}%.")
    # 获取根分区使用情况统计
    total, used, free = shutil.disk_usage("/")
    # 转换成Gib,保留一位小数
    report.append(f"Disk total: {(total / (2 ** 30)): .1f} Gib.")
    report.append(f"Disk used: {(used / (2 ** 30)): .1f} Gib.")
    report.append(f"Disk free: {(free / (2 ** 30)): .1f} Gib.")
	# 列表连成字符串打印
    return ('\n').join(report)

if __name__ == '__main__':
    print(get_system_report())