"""
Kubernetes Pod批量创建脚本

功能描述:
    该脚本使用Kubernetes Python客户端库连接到Kubernetes集群，
    批量创建多个Pod实例。通过编程方式定义Pod规格并循环创建，
    适用于压力测试、批量任务处理、负载测试、开发环境快速部署等场景。

技术实现:
    - kubernetes.config.load_kube_config(): 加载Kubernetes配置
    - kubernetes.client.CoreV1Api(): 创建Core API v1客户端
    - client.V1Pod(): 创建Pod对象定义
    - client.V1ObjectMeta(): 定义Pod元数据
    - client.V1PodSpec(): 定义Pod规格
    - client.V1Container(): 定义容器配置
    - v1.create_namespaced_pod(): 在指定命名空间创建Pod
"""

from kubernetes import config, client

# 导入集群kubeconfig文件
config.load_kube_config(config_file='kubernetes/kubeconfig-local')

# 创建对象
v1 = client.CoreV1Api()
# 用for循环创建pod
for i in range(5):
    pod = client.V1Pod(
        metadata=client.V1ObjectMeta(name=f'my-pod-{i}'),
        spec=client.V1PodSpec(
            containers=[client.V1Container(
                name=f'my-container-{i}',
                image='busybox:1.28',
                command=['sh','-c','sleep 6000']
            )]
        )
    )
    # 创建pod
    v1.create_namespaced_pod(namespace='default',body=pod)