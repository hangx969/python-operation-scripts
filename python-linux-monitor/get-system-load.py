"""
系统负载平均值监控脚本

功能描述:
    该脚本用于获取系统的负载平均值（Load Average），这是衡量系统繁忙程度
    的重要指标。负载平均值反映了在特定时间段内等待CPU处理或等待IO操作
    完成的进程数量，帮助系统管理员评估系统性能和资源使用状况。

技术实现:
    - psutil.getloadavg(): 获取系统负载平均值
      返回元组格式: (load_1min, load_5min, load_15min)
      * load_1min: 最近1分钟的平均负载
      * load_5min: 最近5分钟的平均负载
      * load_15min: 最近15分钟的平均负载

负载平均值含义:
    - 数值表示平均等待处理的进程数量
    - 1.0 = 单核系统满负荷运行
    - 多核系统：负载值可以超过1.0
    - 负载值 < 1.0：系统有空闲资源
    - 负载值 = 1.0：系统满负荷但不过载
    - 负载值 > 1.0：系统过载，有进程等待

输出信息:
    - System load in 1 min: 最近1分钟平均负载
    - System load in 5 min: 最近5分钟平均负载
    - System load in 15 min: 最近15分钟平均负载

"""

import psutil

def get_load():
    # 物理内存使用情况
    load = psutil.getloadavg()
    # 返回元组：(0.5, 0.6, 0.5)，含义是最近1min负载，最近5min负载，最近15min负载
    print(f"System load in 1 min: {load[0]: .2f}.")
    print(f"System load in 5 min: {load[1]: .2f}.")
    print(f"System load in 15 min: {load[2]: .2f}.")

if __name__ == '__main__':
    get_load()