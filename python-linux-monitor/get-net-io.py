"""
网络IO流量监控脚本

功能描述:
    该脚本用于监控系统网络接口的IO流量统计，包括接收和发送的数据量。
    提供累计的网络流量信息，帮助系统管理员了解网络使用情况和流量分布，
    适用于网络性能监控和流量分析。

技术实现:
    - psutil.net_io_counters(): 获取网络IO统计信息
      返回namedtuple包含以下字段：
      * bytes_sent: 发送的总字节数
      * bytes_recv: 接收的总字节数
      * packets_sent: 发送的数据包数量
      * packets_recv: 接收的数据包数量
      * errin/errout: 接收/发送错误计数
      * dropin/dropout: 接收/发送丢包计数
    - 字节到MiB的单位转换（除以2^20）

输出信息:
    - Total received byte: 累计接收的数据量（MiB）
    - Total sent byte: 累计发送的数据量（MiB）

"""

import psutil

def get_net_io():
    net_io = psutil.net_io_counters()
    # net_io_counters()返回namedtuple
    # 类似于：snetio(bytes_sent=1, bytes_recv=3, packets_sent=3, packets_recv=4, errin=0, errout=0, dropin=0, dropout=0)
    print(f"Total received byte: {net_io.bytes_recv / (2 ** 20): .2f} MiB.")
    print(f"Total sent byte: {net_io.bytes_sent / (2 ** 20): .2f} MiB.")


if __name__ == '__main__':
    get_net_io()