"""
邮件日志告警发送脚本

功能描述:
    该脚本演示了如何使用Python的logging模块结合SMTPHandler实现
    日志消息的邮件发送功能。当系统出现错误或关键问题时，会自动
    将日志信息通过邮件发送给指定的收件人，实现实时告警通知。

技术实现:
    - logging.getLogger(): 创建专用的SMTP日志记录器
    - SMTPHandler: 邮件发送处理器
      * mailhost: SMTP服务器地址和端口 ('smtp.163.com', 25)
      * fromaddr: 发件人邮箱地址
      * toaddrs: 收件人邮箱地址列表
      * subject: 邮件主题
      * credentials: SMTP认证凭据 (用户名, 授权码/密码)
      * secure: 安全连接配置
    - logging.Formatter: 邮件内容格式化

SMTP配置说明:
    - mailhost: SMTP服务器配置
      * 网易163邮箱: ('smtp.163.com', 25)
      * QQ邮箱: ('smtp.qq.com', 587)
      * Gmail: ('smtp.gmail.com', 587)
    - credentials: 认证信息
      * 用户名: 完整的邮箱地址或用户名
      * 密码: 邮箱的SMTP授权码（非登录密码）
    - secure: 安全连接
      * (): 不使用安全连接
      * None: 自动检测
      * (): 使用STARTTLS

日志级别配置:
    - 当前设置: logging.ERROR (只发送ERROR和CRITICAL级别日志)
    - ERROR: 错误日志，表示程序遇到问题但仍可继续运行
    - CRITICAL: 严重错误，表示程序可能无法继续运行

邮件格式:
    格式: %(asctime)s-%(name)s-%(levelname)s: %(message)s
    时间格式: %Y%m%d_%H:%M:%S (年月日_时:分:秒)
    示例邮件内容:
    ```
    主题: Error log
    内容: 20250704_14:30:25-smtp_logger-ERROR: This is an error message.
    ```
"""

import logging, os
from logging.handlers import SMTPHandler

os.chdir('/path/to/python/')

# 创建一个日志记录器
logger = logging.getLogger('smtp_logger')
logger.setLevel(logging.ERROR)

# 创建SMTP处理器,password是发件邮箱的smtp的授权码
smtp_handler = SMTPHandler(mailhost=('smtp.163.com', 25),
                           fromaddr='xxxxxx@163.com',
                           toaddrs=['xxxxx@qq.com'],
                           subject="Error log",
                           credentials=('user','password'),
                           secure=()
                           )

# 创建格式化器
formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s: %(message)s', datefmt='%Y%m%d_%H:%M:%S')
smtp_handler.setFormatter(formatter)

# 将处理器添加到记录器上
logger.addHandler(smtp_handler)

# 记录日志，每一条日志独立发送
logger.error(f'This is an error message.')
logger.critical(f'This is an critical message.')