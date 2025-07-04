"""
Kubernetes Pod实时监控脚本

功能描述:
    该脚本使用Kubernetes Python客户端库连接到Kubernetes集群，
    实时监控并显示集群中所有命名空间下的Pod状态信息。通过定时轮询
    的方式持续监控Pod的运行状态，适用于集群监控、故障排查、
    实时状态跟踪等运维场景。

技术实现:
    - kubernetes.config.load_kube_config(): 加载Kubernetes配置
    - kubernetes.client.CoreV1Api(): 创建Core API v1客户端
    - v1.list_pod_for_all_namespaces(): 获取所有命名空间的Pod列表
      * 返回V1PodList对象，包含所有Pod的详细信息
    - time.sleep(60): 设置60秒监控间隔
    - 无限循环实现持续监控
"""

from kubernetes import config, client
import time

# 导入集群kubeconfig文件
config.load_kube_config(config_file='kubernetes/kubeconfig-local')
# 创建对象
v1 = client.CoreV1Api()

while True:
    pods = v1.list_pod_for_all_namespaces()
    for pod in pods.items:
        print(f"Pod Name: {pod.metadata.name} - Status: {pod.status.phase}")
    time.sleep(60)