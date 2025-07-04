"""
系统内存使用情况监控脚本

功能描述:
    该脚本用于监控系统的内存使用情况，包括物理内存（RAM）和虚拟内存
    （交换分区/页面文件）的使用状态。提供详细的内存统计信息，帮助
    系统管理员了解内存资源使用情况和系统性能状态。

技术实现:
    - psutil.virtual_memory(): 获取物理内存使用情况
      返回namedtuple包含: total, available, percent, used, free等字段
    - psutil.swap_memory(): 获取交换分区使用情况
      返回namedtuple包含: total, used, free, percent等字段
    - 字节到GiB的单位转换（除以2^30）

输出信息:
    物理内存部分:
    - Total memory: 总物理内存容量（GiB）
    - Used memory: 已使用物理内存（GiB）
    - Available memory: 可用物理内存（GiB）

    交换分区部分:
    - Total swap: 总交换分区容量（GiB）
    - Used swap: 已使用交换分区（GiB）
    - Available swap: 可用交换分区（GiB）

"""

import psutil

def get_memory():
    # 物理内存使用情况
    mem_usage = psutil.virtual_memory()
    # 返回namedtuple：svmem(total=3, available=2, percent=34.2, used=1, free=1, active=1, inactive=3, buffers=5, cached=7, shared=4, slab=1)
    print(f"Total memory: {mem_usage.total / (2 ** 30) : .2f} GiB.")
    print(f"Used memory: {mem_usage.used / (2 ** 30) : .2f} GiB.")
    print(f"Available memory: {mem_usage.free / (2 ** 30) : .2f} GiB.")

    # 交换分区使用情况
    swap_usage = psutil.swap_memory()
    print(f"Total swap: {swap_usage.total / (2 ** 30) : .2f} GiB.")
    print(f"Used swap: {swap_usage.used / (2 ** 30) : .2f} GiB.")
    print(f"Available swap: {swap_usage.free / (2 ** 30) : .2f} GiB.")

if __name__ == '__main__':
    get_memory()