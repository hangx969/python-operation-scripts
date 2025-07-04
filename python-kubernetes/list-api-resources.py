"""
Kubernetes API资源获取脚本

功能描述:
    该脚本使用Kubernetes Python客户端库连接到Kubernetes集群，
    并获取集群中所有可用的API资源信息。适用于集群API探索、
    资源类型查询、API版本检查等运维和开发场景。

技术实现:
    - kubernetes.config.load_kube_config(): 加载Kubernetes配置
      * config_file参数: 指定kubeconfig文件路径
      * 默认会查找~/.kube/config文件
    - kubernetes.client.CoreV1Api(): 创建Core API v1客户端
      * 提供对核心Kubernetes资源的访问
    - v1.get_api_resources(): 获取所有API资源列表
"""

from kubernetes import config, client
# 导入集群kubeconfig文件
config.load_kube_config(config_file='kubernetes/kubeconfig-local')
# 创建对象
v1 = client.CoreV1Api()

# 获取所有api资源
print(v1.get_api_resources())