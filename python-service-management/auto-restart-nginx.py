"""
Nginx服务自动重启脚本

功能描述:
    该脚本用于自动检查Nginx服务的运行状态，当发现Nginx服务未运行时，
    自动执行重启操作。通过systemctl命令与系统服务管理器交互，
    实现智能的服务健康检查和自动恢复功能。适用于服务监控、
    自动化运维、服务保活等场景。

技术实现:
    - subprocess.run(): 执行系统命令
    - systemctl is-active: 检查服务运行状态
    - systemctl restart: 重启服务
    - 返回值类型注解: -> bool, -> None
    - 异常处理: subprocess.CalledProcessError

"""

import subprocess

def check_nginx_alive() -> bool:
    try:
        result = subprocess.run(['systemctl','is-active', 'nginx'], capture_output=True, text=True, check=True)
        return result.stdout.strip() == 'active' # 是active就返回True，否则就返回False
    except subprocess.CalledProcessError as e: # 命令执行失败直接返回False
        return False

def restart_nginx() -> None:
    try:
        subprocess.run(['systemctl','restart', 'nginx'], capture_output=True, text=True, check=True)
        print("Nginx is restarted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to restart nginx: {e.stderr}.")

if __name__ == '__main__':
    if not check_nginx_alive():
        print(f"Nginx is not running, restarting nginx.")
        restart_nginx()
    else:
        print('Nginx is already running.')