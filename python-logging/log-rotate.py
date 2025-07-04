"""
日志轮替（Log Rotation）管理脚本

功能描述:
    该脚本演示了如何使用Python的logging模块实现日志轮替功能。
    当日志文件达到指定大小时，系统会自动创建新的日志文件，并保留
    指定数量的历史日志文件，防止单个日志文件过大占用过多磁盘空间。

技术实现:
    - logging.getLogger(): 创建日志记录器
    - RotatingFileHandler: 日志轮替处理器
      * maxBytes=2000: 单个日志文件最大2000字节
      * backupCount=5: 最多保留5个历史日志文件
      * encoding='utf-8': 使用UTF-8编码
    - logging.Formatter: 自定义日志格式化器
    - 时间格式: '%Y%m%d_%H:%M:%S' (年月日_时:分:秒)

日志轮替机制:
    1. 当前日志文件: my_log.log
    2. 文件大小达到2000字节时触发轮替
    3. 当前文件重命名为: my_log.log.1
    4. 创建新的空白 my_log.log 文件
    5. 历史文件按序号递增: my_log.log.1, my_log.log.2, ...
    6. 超过backupCount(5)的旧文件会被自动删除

日志格式说明:
    格式: %(asctime)s-%(name)s-%(levelname)s: %(message)s
    示例: 20250704_14:30:25-rotating_logger-DEBUG: This is number 1 message.

    组成部分:
    - %(asctime)s: 时间戳
    - %(name)s: 日志记录器名称
    - %(levelname)s: 日志级别
    - %(message)s: 日志消息内容

"""

import logging, os
from logging.handlers import RotatingFileHandler

os.chdir('/path/to/logs/')

# 创建一个日志记录器
logger = logging.getLogger('rotating_logger')
logger.setLevel(logging.DEBUG)

# 创建日志轮替处理器
# maxBytes=2000: 当文件大小达到2000字节，触发日志轮替
# backupCount = 5 最多保留五个旧的日志文件（my_log.log1 ... my_log.log5）
# encoding = 'utf-8' 文件使用UTF-8编码，避免中文乱码
rotating_handler = RotatingFileHandler('my_log.log', maxBytes=2000,backupCount=5,encoding='utf-8')

# 创建格式化器
formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s: %(message)s', datefmt='%Y%m%d_%H:%M:%S')
# 对处理器应用这个格式
rotating_handler.setFormatter(formatter)

# 将处理器添加到记录器上
logger.addHandler(rotating_handler)

# 记录日志，观察日志轮替的生成文件的结果
for i in range(1000):
    logger.debug(f'This is number {i} message.')