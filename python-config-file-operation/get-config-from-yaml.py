"""
YAML配置信息批量提取脚本

功能描述:
    该脚本用于从指定目录中的多个YAML配置文件中批量提取关键信息，
    如服务名称和容器镜像版本等。特别适用于Kubernetes环境中的
    配置审计、版本清单生成、资源盘点等场景。

技术实现:
    - os.listdir(): 遍历指定目录中的所有文件
    - file.endswith('.yaml'): 过滤YAML文件
    - yaml.safe_load(): 安全地解析YAML文件内容
    - os.path.join(): 构建完整的文件路径
    - 字典嵌套访问: 提取深层嵌套的配置字段
"""

# 从两个yaml文件中获取到deployment的name和image
import yaml, os

def get_config(yaml_dir):
    report = []
    for file in os.listdir(yaml_dir):
        if file.endswith('.yaml'):
            # 把yaml文件读取成字典
            with open(os.path.join(yaml_dir,file), 'r') as f:
                config = yaml.safe_load(f)
            # 获取字典键值
            name = config['metadata']['name']
            image = config['spec']['template']['spec']['containers'][0]['image']
            # 列表中直接把编写好的字符串放进去
            report.append(f"Service name: {name}, image version: {image}")
    return report

if __name__ == '__main__':
    os.chdir('Python/python-manuscripts')
    yaml_dir = 'configs'
    report = get_config(yaml_dir)
    for line in report:
        print(line)