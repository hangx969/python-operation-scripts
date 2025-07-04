"""
YAML配置文件批量更新脚本

功能描述:
    该脚本用于批量更新多个YAML配置文件中的特定字段值，特别适用于
    Kubernetes环境中的容器镜像版本更新、配置参数批量修改等场景。
    通过函数化设计，实现了对多个服务配置文件的统一管理和更新。

技术实现:
    - yaml.safe_load(): 安全地读取YAML文件内容
    - yaml.safe_dump(): 安全地将Python对象序列化为YAML格式
    - 字典嵌套访问: 通过键链访问深层嵌套字段
    - 列表索引操作: 访问containers列表中的特定容器
    - 文件上下文管理: 确保文件正确关闭
"""

import yaml

def update_yaml(yaml_file, new_image):
    # 读取yaml文件转成python字典
    with open(yaml_file, 'r') as f:
        config = yaml.safe_load(f)
    # 修改python字典里面的image字段，注意containers是一个列表需要用下标找到第一个字典元素
    config['spec']['template']['spec']['containers'][0]['image'] = new_image
    # 把改完的字典序列化回到文件
    with open(yaml_file, 'w') as f:
        yaml.safe_dump(config, f)

if __name__ == '__main__':
    update_yaml('python-manuscripts/service1.yaml', 'janakiramm/myapp:v2')
    update_yaml('python-manuscripts/service2.yaml', 'janakiramm/myapp:v2')