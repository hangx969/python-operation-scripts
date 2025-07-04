"""
Kubernetes命名空间列表获取脚本

功能描述:
    该脚本使用Kubernetes Python客户端库连接到Kubernetes集群，
    获取并显示集群中所有命名空间的信息。提供了两种方式来获取
    命名空间列表：直接遍历和函数封装，适用于多租户管理、
    资源隔离查看、命名空间审计等场景。

技术实现:
    - kubernetes.config.load_kube_config(): 加载Kubernetes配置
    - kubernetes.client.CoreV1Api(): 创建Core API v1客户端
    - v1.list_namespace(): 获取所有命名空间列表
      * 返回V1NamespaceList对象，包含所有命名空间详细信息
    - namespaces.items: 命名空间列表，每个元素为V1Namespace对象
    - ns.metadata.name: 获取命名空间名称
"""

from kubernetes import config, client
# 导入集群kubeconfig文件
config.load_kube_config(config_file='kubernetes/kubeconfig-local')
# 创建对象
v1 = client.CoreV1Api()

# 返回的是一个对象，包含所有ns的json属性
namespaces = v1.list_namespace()
# for ns in namespaces.items:
#     print(ns)

for ns in namespaces.items:
    # 打印每个ns的name
    print(ns.metadata.name)

# 用函数获取集群namespace
def get_namespace():
    return [ns.metadata.name for ns in v1.list_namespace().items]

if __name__ == '__main__':
    ns_list = get_namespace()
    for ns in ns_list:
        print(ns)