#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Apache HTTP 服务器远程管理图形界面工具

功能描述:
    本脚本提供基于 Tkinter 的图形用户界面，用于远程管理 Apache HTTP 服务器 (httpd)。
    通过 SSH 连接到远程服务器，实现 Apache 服务的启动、停止、状态查询和日志查看操作，
    为 Web 服务器运维人员提供直观便捷的服务管理工具。

技术实现:
    - 使用 Tkinter 构建桌面图形用户界面
    - 使用 paramiko 库建立 SSH 连接和远程命令执行
    - 采用 systemctl 命令管理 systemd 服务
    - 使用 pack() 布局管理器组织界面元素
    - 通过 ScrolledText 组件显示日志内容

界面组件设计:
    1. 状态标签 - 显示当前服务状态提示文本
    2. 状态文本框 - 显示 "Running" 或 "Not Running" 状态
    3. 状态检查按钮 - 执行 systemctl status httpd 命令
    4. 启动服务按钮 - 执行 systemctl start httpd 命令
    5. 停止服务按钮 - 执行 systemctl stop httpd 命令
    6. 查看日志按钮 - 显示 Apache 访问日志内容
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
import paramiko

HOST = '192.168.40.80'
USERNAME = 'root'
PASSWD = '111111'
HTTPD_SERVICE = 'httpd'
LOG_PATH = '/var/log/httpd/access.log'

def create_ssh_client():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USERNAME, password=PASSWD)
        return client
    except Exception as e:
        messagebox.showerror('Error', f"Failed to connect SSH: {str(e)}\n")
        return None

def check_status():
    client = create_ssh_client()
    if client:
        stdin, stdout, stderr = client.exec_command(f'systemctl status {HTTPD_SERVICE}')
        output = stdout.read().decode()
        if "running" in str(output):
            status_text.delete(1.0, tk.END)
            status_text.insert(tk.END, 'Running')
        else:
            status_text.delete(1.0, tk.END)
            status_text.insert(tk.END, 'Not Running')
        client.close()

def start_service():
    client = create_ssh_client()
    if client:
        try:
            stdin, stdout, stderr = client.exec_command(f'systemctl start {HTTPD_SERVICE}')
            error = stderr.read().decode()
            if error:
                messagebox.showerror("Error", f"Failed to start httpd: {error}\n")
            else:
                messagebox.showinfo('Info', 'Httpd has been started\n')
        finally:
            client.close()

def stop_service():
    client = create_ssh_client()
    if client:
        try:
            stdin, stdout, stderr = client.exec_command(f'systemctl stop {HTTPD_SERVICE}')
            error = stderr.read().decode()
            if error:
                messagebox.showerror("Error", f"Failed to stop httpd: {error}\n")
            else:
                messagebox.showinfo('Info', 'Httpd has been stopped\n')
        finally:
            client.close()

def view_log():
    client = create_ssh_client()
    if client:
        stdin, stdout, stderr = client.exec_command(f'cat {LOG_PATH}')
        error = stderr.read().decode()
        if error:
            messagebox.showerror("Error", f"Failed to get httpd log: {error}\n")
        else:
            log_content = stdout.read().decode()
            log_window = tk.Toplevel(root)
            log_window.title('Httpd logs')
            log_text = scrolledtext.ScrolledText(log_window, height=20, width=80)
            log_text.pack()
            log_text.insert(tk.END, log_content)
        client.close()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Httpd service management")

    status_label = tk.Label(root, text='httpd service status:')
    status_label.pack()
    status_text = tk.Text(root, height=1, width=30)
    status_text.pack()

    check_status_button = tk.Button(root, text='Check status', command=check_status)
    check_status_button.pack()

    start_button = tk.Button(root, text='start service', command=start_service)
    start_button.pack()

    stop_button = tk.Button(root, text='stop service', command=stop_service)
    stop_button.pack()

    log_button = tk.Button(root, text='check logs', command=view_log)
    log_button.pack()

    root.mainloop()
