"""
磁盘分区使用情况监控脚本

功能描述:
    该脚本用于监控系统中所有磁盘分区的使用情况，包括总容量、已使用空间、
    剩余空间和使用百分比。提供详细的磁盘空间统计信息，便于系统管理员
    进行磁盘空间管理和监控。

技术实现:
    - psutil.disk_partitions(): 获取所有磁盘分区信息
    - psutil.disk_usage(): 获取指定挂载点的使用情况
    - 字节到GiB的单位转换（除以2^30）
    - namedtuple数据结构处理

输出信息:
    - Mount point: 挂载点路径
    - Total: 总容量（GiB）
    - Used: 已使用空间（GiB）
    - Free: 剩余空间（GiB）
    - Used percentage: 使用百分比
"""

import psutil

def get_disk_usage():
    # disk_partition()方法返回一个列表，里面是分区信息的元组 - namedtuple：
    # 类似于[sdiskpart(device='/dev/vg00/root', mountpoint='/', fstype='ext4', opts='rw')]
    part_usage = psutil.disk_partitions()

    # 遍历分区元组，获取其中mountpoint参数，让psutil.disk_usage计算使用情况
    for part in part_usage:
        # disk_usage方法获取到一个namedtuple，类似于：sdiskusage(total=1046, used=520, free=99, percent=5.0)
        usage = psutil.disk_usage(part.mountpoint)

        # 单位转换，字节转换为Gib，除以2的30次方（1 Gib的字节数）
        # 如果要转换为GB, 除以1024**3
        total_gb = usage.total / (2 ** 30)
        used_gb = usage.used / (2 ** 30)
        free_gb = usage.free / (2 ** 30)
        used_percentage = usage.used / usage.total * 100
        print(f"Mount point: {part.mountpoint}")
        print(f"Total: {total_gb: .2f} GiB")
        print(f"Used: {used_gb: .2f} GiB")
        print(f"Free: {free_gb: .2f} GiB")
        print(f"Used percentage: {used_percentage: .1f}%")
        print('-' * 30)

if __name__ == '__main__':
    get_disk_usage()