"""
YAML配置文件管理脚本

功能描述:
    该脚本演示了如何使用Python的PyYAML库读取和解析YAML格式的配置文件。
    特别适用于处理Kubernetes部署文件、Docker Compose配置、CI/CD配置等
    复杂的嵌套结构配置文件，提供了安全可靠的YAML数据访问方法。

技术实现:
    - yaml.safe_load(): 安全地加载YAML文件内容
      * 相比yaml.load()更安全，防止执行恶意代码
      * 将YAML内容转换为Python对象（字典、列表等）
    - 字典键值访问: 使用键名逐层访问嵌套数据
    - 列表索引访问: 使用数字索引访问列表元素

"""

import yaml

with open('python-manuscripts/deployment.yaml', 'r') as f:
    config = yaml.safe_load(f)

# 获取某些值，用字典key来获取
replicas = config['spec']['replicas']
print(replicas)

# 注意containers是一个列表，里面元素是一个一个的字典，第一个container的序号是0
image = config['spec']['template']['spec']['containers'][0]['image']
print(image)