"""
Tomcat 服务自动重启监控脚本

功能描述:
    本脚本用于监控 Tomcat 服务的运行状态，当检测到 Tomcat 服务停止时自动重启服务。
    通过持续的服务状态检查和自动恢复机制，确保 Tomcat 服务的高可用性。

技术实现:
    - 使用 subprocess 模块执行系统命令
    - 通过 ps aux + grep 组合命令检测进程
    - 使用 catalina.sh 脚本启动 Tomcat 服务
    - 基于时间间隔的循环监控机制
"""

import time, subprocess

def check_tomcat() -> bool:
    try:
        # grep 要把grep和python脚本本身的进程排除出去
        result = subprocess.run("ps aux | grep tomcat | grep -v grep | grep -v python", shell=True, capture_output=True, check=True, text=True)
        if result.stdout:
            print("Tomcat is running.")
            return True
        else:
            print("Tomcat is not running")
            return False
    except Exception as e:
        print(f"An error occurred while checking Tomcat status: {e}.")
        return False

def start_tomcat():
    try:
        tomcat_start_command="/opt/tomcat/bin/catalina.sh start"
        result = subprocess.run(tomcat_start_command, shell=True, text=True, capture_output=True, check=True)
        if result.returncode == 0:
            print("Tomcat started successfully.")
        else:
            print("Failed to start tomcat.")
    except Exception as e:
        print(f"{e}")

def monitor_tomcat(interval):
    while True:
        if not check_tomcat():
            start_tomcat()
        else:
            print("No action needed, tomcat is running.")
        time.sleep(interval)

if __name__ == '__main__':
    monitor_tomcat(60)