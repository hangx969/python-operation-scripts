"""
Nginx配置文件语法检查脚本

功能描述:
    该脚本用于检查Nginx配置文件的语法正确性，通过调用nginx命令行工具
    的测试功能来验证配置文件是否存在语法错误。适用于配置文件修改后的
    验证、自动化部署流程、运维检查等场景，能够在重载配置前确保配置正确性。

技术实现:
    - subprocess.run(): 执行系统命令
      * command: ['nginx', '-t'] - 调用nginx测试命令
      * capture_output=True: 捕获命令输出
      * text=True: 以文本形式处理输出
      * check=True: 命令失败时抛出异常
    - subprocess.CalledProcessError: 捕获命令执行失败异常
    - e.stderr: 获取错误输出信息

"""

import subprocess

def check_nginx_config():
    try:
        subprocess.run(['nginx','-t'], capture_output=True, text=True, check=True)
        print("Nginx config is correct.")
    # subprocess.CalledProcessError 表示指定的命令运行失败了
    except subprocess.CalledProcessError as e:
        print(e.stderr)

if __name__ == '__main__':
    check_nginx_config()