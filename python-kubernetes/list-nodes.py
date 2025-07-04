"""
Kubernetes节点列表获取脚本

功能描述:
    该脚本使用Kubernetes Python客户端库连接到Kubernetes集群，
    获取并显示集群中所有节点的基本信息。适用于集群节点监控、
    资源盘点、节点状态检查等运维管理场景。

技术实现:
    - kubernetes.config.load_kube_config(): 加载Kubernetes配置
    - kubernetes.client.CoreV1Api(): 创建Core API v1客户端
    - v1.list_node(): 获取所有节点列表
      * 返回V1NodeList对象，包含所有节点的详细信息
    - nodes.items: 节点列表，每个元素为V1Node对象
    - node.metadata.name: 获取节点名称

"""

from kubernetes import config, client
# 导入集群kubeconfig文件
config.load_kube_config(config_file='kubernetes/kubeconfig-local')
# 创建对象
v1 = client.CoreV1Api()

# 获取所有节点列表
# 返回的是一个V1NodeList对象，包含所有node详细信息，metadata、statua等
nodes = v1.list_node()

# nodes.items是一个V1Node对象，包含某个node的信息
for node in nodes.items:
    # node.metadata.name获取到这个node的name属性值。层级路径和yaml文件中的层级路径一样
    print(f"Node name: {node.metadata.name}")