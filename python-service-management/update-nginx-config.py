"""
Nginx配置文件动态更新脚本

功能描述:
    该脚本用于动态添加新的server块到Nginx配置文件中，并自动重载
    Nginx服务以使配置生效。通过编程方式管理Nginx配置，避免手动
    编辑配置文件的繁琐和错误风险。适用于自动化部署、动态站点管理、
    反向代理配置等场景。

技术实现:
    - 文件操作: open(file_path, 'a') - 追加模式写入配置
    - 服务管理: systemctl reload nginx - 重载配置不中断服务
    - 异常处理: subprocess.CalledProcessError - 捕获命令执行失败
    - 类型注解: -> None - 明确函数返回类型

"""

import subprocess

def add_server_block(file_path, server_block) -> None:
    with open(file_path, 'a') as f:
        f.write(server_block)
    print("New server block has been added to nginx config file.")

def reload_nginx() -> None:
    try:
        result = subprocess.run(['systemctl','reload', 'nginx'], capture_output=True, text=True, check=True)
        print("Nginx is reloaded successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to reload nginx: {e.stderr}.")

if __name__ == '__main__':
    config = '/etc/nginx/nginx.conf'
    new_server_block = """
    server {
    listen 8080;
    server_name example.com;
    location / {
        proxy_pass http://localhost:8000;
    }
    }
    """

    add_server_block(config, new_server_block)
    reload_nginx()
