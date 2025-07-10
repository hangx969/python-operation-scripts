"""
Kubernetes 镜像批量传输和加载工具

功能描述:
    该脚本用于自动化批量传输和加载 Kubernetes 镜像到多个远程主机。
    主要实现以下功能：

    1. SSH 连接管理
       - 批量连接多个 Kubernetes 节点
       - 支持用户名密码认证
       - 自动处理主机密钥策略

    2. SFTP 文件传输
       - 将本地 Docker 镜像 tar 包传输到远程主机
       - 支持大文件传输
       - 完善的异常处理和状态反馈

    3. 镜像加载
       - 使用 containerd 的 ctr 命令导入镜像
       - 支持 Kubernetes 命名空间 (k8s.io)
       - 实时显示加载状态和结果

    4. 批量处理
       - 支持多个镜像文件的批量处理
       - 支持多个目标主机的并行操作

工作流程:
    1. 检查并创建本地镜像存储目录
    2. 遍历目标主机列表
    3. 建立 SSH 连接
    4. 扫描本地 .tar 镜像文件
    5. 逐个传输镜像到远程主机
    6. 在远程主机上导入镜像到 containerd
    8. 关闭连接，处理下一台主机

使用场景:
    - Kubernetes 集群离线镜像部署
    - 容器镜像在多节点间的快速分发
    - 开发环境镜像同步
    - 生产环境镜像批量更新

配置要求:
    - 远程主机已安装 containerd
    - SSH 服务正常运行
    - 具有 root 权限或 containerd 操作权限
    - 网络连接稳定
"""

import os, paramiko

def ssh_connect(host):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        client.connect(hostname=host, username='root', password='root')
        return client
    except Exception as e:
        print(f"Error: {str(e)}.")
        return None


def transfer_image(client, local_file, remote_file):
    try:
        sftp = client.open_sftp()
        sftp.put(local_file, remote_file)
        print(f"\n\nFiles transferred from {local_file} to {remote_file}.")
    except Exception as e:
        print(f"Error: {str(e)}.")
    finally:
        sftp.close()


def load_image(client, image_path):
    stdin, stdout, stderr = client.exec_command(f"ctr -n=k8s.io images import {image_path}")
    # 获取返回状态码
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        print(f"{image_path} loaded")
        output = stdout.read().decode('utf-8').strip()
        if output:
            print(f"Output: {output}")
    else:
        error_msg = stderr.read().decode('utf-8').strip()
        print(f"Error loading {image_path}: {error_msg}.")



if __name__ == '__main__':

    local_path = r"D:\InstallationPackages\k8s-images"
    remote_path = "/root/"
    hosts = ['192.168.40.180','192.168.40.181','192.168.40.182']

    # 检查本地路径是否存在
    if not os.path.exists(local_path):
        print(f"{local_path} does not exist, creating...")
        os.makedirs(local_path)

    for host in hosts:
        # 建立ssh连接
        client = ssh_connect(host)
        if not client:
            print(f"Error connected to {host}")
            break

        print(f"\n\nConnected to {host}")

        # 对每个tar镜像，先传输，再解压
        for image in os.listdir(local_path):
            if image.endswith(".tar"):
                local_file = os.path.join(local_path,image)
                remote_file = os.path.join(remote_path, image)
                # sftp传输镜像文件
                transfer_image(client, local_file, remote_file)
                # 远程主机解压镜像
                load_image(client, remote_file)
        client.close()
