"""
SFTP远程文件传输脚本

功能描述:
    该脚本使用paramiko库实现SSH/SFTP协议的远程文件传输功能。
    支持向远程服务器上传文件和从远程服务器下载文件，适用于
    自动化部署、文件同步、备份传输等场景。

技术实现:
    - paramiko.SSHClient(): 创建SSH客户端连接
    - ssh.set_missing_host_key_policy(): 设置主机密钥策略
      * AutoAddPolicy: 自动接受未知主机密钥
    - ssh.connect(): 建立SSH连接
    - ssh.open_sftp(): 创建SFTP客户端
    - sftp.put(): 上传文件到远程服务器
    - sftp.get(): 从远程服务器下载文件

连接参数说明:
    - hostname: 远程服务器IP地址或域名
    - port: SSH服务端口（默认22）
    - username: 远程服务器用户名
    - password: 远程服务器密码
    - local_path: 本地文件完整路径
    - remote_path: 远程文件完整路径

文件操作流程:
    1. 创建SSH客户端并设置密钥策略
    2. 准备本地文件路径和远程路径
    3. 检查并创建本地目录
    4. 如果本地文件不存在，创建测试文件
    5. 建立SSH连接到远程服务器
    6. 打开SFTP会话
    7. 执行文件传输操作
    8. 关闭SFTP和SSH连接

"""

import paramiko, os

# 创建ssh客户端
ssh = paramiko.SSHClient()
# 设置自动接受host key
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)

# 准备本地文件路径
# 如果是windows上，local_dir可以写成'D:/'
local_dir = '/path/to/python/'
local_file = 'oop.py'
local_path = os.path.join(local_dir,local_file)

# 连接到的远程服务器
hostname = '1.2.3.4'
port = 22
username = 'root'
password = 'root'
# 远程路径必须要具体到文件名才能成功sftp put。
remote_path = '/root/oop.py'

try:
    # 创建本地目录，检查本地文件
    os.makedirs(local_dir, exist_ok=True)
    if not os.path.exists(local_path):
        with open(local_path, 'w') as f:
            f.write("test")
        print(f"File {local_path} has been created.")

    # 创建ssh客户端
    ssh.connect(hostname, port, username, password)
    print(f"Connected to {hostname}.")
    # 创建sftp客户端
    sftp = ssh.open_sftp()
    # sftp上传文件
    sftp.put(local_path, remote_path)
    print(f"File transferred from {local_path} to {remote_path}.")

    # sftp下载文件
    # sftp.get(remote_path, local_path)

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    # paramiko模块需要手动关闭ssh和sftp连接
    sftp.close()
    ssh.close()
    print("Connection has closed.")