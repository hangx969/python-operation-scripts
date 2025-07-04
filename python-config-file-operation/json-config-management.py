"""
JSON配置文件管理脚本

功能描述:
    该脚本演示了如何使用Python的json模块对JSON格式的配置文件进行
    读取、修改和保存操作。提供了一个完整的JSON配置文件管理流程，
    适用于应用程序配置管理、系统参数调整等场景。

技术实现:
    - json.load(): 从文件中读取JSON数据并反序列化为Python对象
    - json.dump(): 将Python对象序列化并写入JSON文件
    - 字典操作: 使用键值对方式修改配置项
    - 文件上下文管理: 使用with语句确保文件正确关闭
    - indent参数: 设置JSON输出格式缩进，提高可读性

配置文件操作流程:
    1. 打开并读取JSON配置文件
    2. 使用json.load()将JSON内容反序列化为Python字典
    3. 通过字典键值访问和修改配置项
    4. 支持嵌套字典的深层字段修改
    5. 使用json.dump()将修改后的字典序列化回JSON格式
    6. 保存到原文件或新文件中

"""

import json

# 有一个json配置文件，需要修改其中的字段：
# 1. 读取json文件
# 2. 反序列化成python对象
# 3. 修改字段
# 4. 序列化到文件中

# 读取json文件并反序列化成字典
with open('python-manuscripts/config.json', 'r') as f:
    config = json.load(f)

# 字典赋值的方法来修改字段
config['version'] = '1.0.1'
config['logging']['level'] = 'DEBUG'
config['notifications']['email']['username'] = 'test_user'

# 序列化到json文件
with open('python-manuscripts/config.json', 'w') as f:
    json.dump(config, f, indent=4)