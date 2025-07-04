"""
Kubernetes Deployment容器镜像批量更新脚本

功能描述:
    该脚本用于批量更新多个命名空间中Deployment的容器镜像版本。
    通过遍历指定的命名空间列表，检查目标Deployment的当前镜像版本，
    并将符合条件的旧镜像自动更新为新镜像。适用于版本升级、
    安全补丁应用、统一镜像管理等运维场景。

技术实现:
    - kubernetes.client.AppsV1Api(): 创建Apps API v1客户端
    - appsv1.read_namespaced_deployment(): 读取现有Deployment配置
    - appsv1.patch_namespaced_deployment(): 更新Deployment配置
    - 容器镜像路径访问: dep.spec.template.spec.containers[0].image
    - 异常处理: 捕获API调用异常

"""

from kubernetes import client, config
# 导入集群kubeconfig文件
config.load_kube_config(config_file='kubernetes/kubeconfig-local')
# 创建对象
appsv1 = client.AppsV1Api()

namespaces = ['qatest','development','production']
old_image = 'busybox:1.28'
new_image = 'busybox:latest'
deployment_name = 'my-deployment'

for ns in namespaces:
    try:
        dep = appsv1.read_namespaced_deployment(name=deployment_name, namespace=ns)
        current_image = dep.spec.template.spec.containers[0].image

        if current_image == old_image:
            print(f"Namespace: {ns}, deployment: {deployment_name}, updating image from {old_image} to {new_image}.")
            dep.spec.template.spec.containers[0].image = new_image
            appsv1.patch_namespaced_deployment(name=deployment_name, namespace=ns, body=dep)
            print(f"Namespace: {ns}, deployment: {deployment_name}, updated image from {old_image} to {new_image}.")

        else:
            print(f"Namespace: {ns}, deployment {deployment_name}, image has already been up-to-date.")

    except client.exceptions.ApiException as e:
        print(f"Error: {str(e)}")