# python-operation-scripts
This is a repo for python scripts to automate Linux and Kubernetes management

## 脚本一览表

### Linux 系统监控

| 脚本路径 | 功能简介 |
|---------|---------|
| [backup-files-to-dir.py](./python-linux-monitor-operation/backup-files-to-dir.py) | 文件备份工具，将指定文件或目录备份到目标位置 |
| [check-missing-parameters.py](./python-linux-monitor-operation/check-missing-parameters.py) | 检查系统配置或脚本参数的完整性，确保必要参数不缺失 |
| [check-server-alive.py](./python-linux-monitor-operation/check-server-alive.py) | 持续监控多个服务器的网络连通性，通过 ping 命令检测服务器存活状态 |
| [get-disk-partition.py](./python-linux-monitor-operation/get-disk-partition.py) | 获取系统磁盘分区信息，包括分区大小、挂载点和文件系统类型 |
| [get-filesystem-cpu-memory-usage.py](./python-linux-monitor-operation/get-filesystem-cpu-memory-usage.py) | 生成系统综合监控报告，集成 CPU、内存和磁盘使用情况 |
| [get-linux-disk-usage.py](./python-linux-monitor-operation/get-linux-disk-usage.py) | 监控 Linux 系统磁盘空间使用情况，支持多磁盘和分区监控 |
| [get-memory-usage.py](./python-linux-monitor-operation/get-memory-usage.py) | 实时获取系统内存使用率，包括物理内存和交换空间信息 |
| [get-multi-core-cpu-usage.py](./python-linux-monitor-operation/get-multi-core-cpu-usage.py) | 监控多核 CPU 的使用率，提供每个 CPU 核心的详细使用情况 |
| [get-net-io.py](./python-linux-monitor-operation/get-net-io.py) | 监控网络接口的 I/O 统计信息，包括流量和数据包统计 |
| [get-process-pid.py](./python-linux-monitor-operation/get-process-pid.py) | 根据进程名称查找对应的进程 ID，用于进程管理和监控 |
| [get-system-load.py](./python-linux-monitor-operation/get-system-load.py) | 获取系统负载平均值，监控系统整体性能状态 |
| [rename-file-ext.py](./python-linux-monitor-operation/rename-file-ext.py) | 批量修改文件扩展名，支持正则表达式匹配和替换 |
| [sftp-send-files-to-remote.py](./python-linux-monitor-operation/sftp-send-files-to-remote.py) | 通过 SFTP 协议向远程服务器传输文件，支持批量文件传输 |

### Kubernetes 管理

| 脚本路径 | 功能简介 |
|---------|---------|
| [create-pods-in-scale.py](./python-kubernetes/create-pods-in-scale.py) | 批量创建 Kubernetes Pod 实例，适用于压力测试和负载测试场景 |
| [deployment-statefulset-manager-GUI.py](./python-kubernetes/deployment-statefulset-manager-GUI.py) | 基于 Tkinter 的 K8s Deployment 和 StatefulSet 副本数管理图形界面工具 |
| [list-all-pods.py](./python-kubernetes/list-all-pods.py) | 列出 Kubernetes 集群中所有 Pod 的详细信息，包括状态和资源使用情况 |
| [list-api-resources.py](./python-kubernetes/list-api-resources.py) | 获取 Kubernetes 集群支持的所有 API 资源类型和版本信息 |
| [list-namespaces.py](./python-kubernetes/list-namespaces.py) | 列出 Kubernetes 集群中所有命名空间及其状态信息 |
| [list-nodes.py](./python-kubernetes/list-nodes.py) | 查看 Kubernetes 集群节点信息，包括节点状态和资源容量 |
| [update-images.py](./python-kubernetes/update-images.py) | 批量更新 Kubernetes 工作负载的容器镜像版本 |
| [update-replica.py](./python-kubernetes/update-replica.py) | 动态调整 Kubernetes Deployment 或 StatefulSet 的副本数量 |

### 服务管理

| 脚本路径 | 功能简介 |
|---------|---------|
| [auto-restart-elasticsearch.py](./python-service-management/auto-restart-elasticsearch.py) | Elasticsearch 服务自动重启脚本，监控服务状态并在异常时自动重启 |
| [auto-restart-nginx.py](./python-service-management/auto-restart-nginx.py) | Nginx 服务自动重启脚本，实现智能的服务健康检查和自动恢复功能 |
| [auto-restart-tomcat.py](./python-service-management/auto-restart-tomcat.py) | Tomcat 服务自动重启脚本，确保 Web 应用服务的高可用性 |
| [check-nginx-config.py](./python-service-management/check-nginx-config.py) | Nginx 配置文件语法检查工具，验证配置文件的正确性 |
| [httpd-manager-GUI.py](./python-service-management/httpd-manager-GUI.py) | Apache HTTP 服务器图形化管理工具，提供服务启停和状态监控功能 |
| [mysql-manager-GUI.py](./python-service-management/mysql-manager-GUI.py) | MySQL 数据库服务图形化管理工具，支持数据库服务的远程管理 |
| [nginx-manager-GUI.py](./python-service-management/nginx-manager-GUI.py) | Nginx 服务图形化管理工具，通过 SSH 远程管理 Nginx 服务 |
| [tomcat-manager-GUI.py](./python-service-management/tomcat-manager-GUI.py) | Tomcat 服务图形化管理工具，提供 Web 应用服务器的远程管理功能 |
| [update-nginx-config.py](./python-service-management/update-nginx-config.py) | Nginx 配置文件更新工具，支持配置文件的动态修改和热重载 |

### 日志管理

| 脚本路径 | 功能简介 |
|---------|---------|
| [clear-old-logs.py](./python-logging/clear-old-logs.py) | 自动清理指定目录下的过期日志文件，基于文件修改时间进行清理 |
| [log-rotate.py](./python-logging/log-rotate.py) | 日志轮转工具，实现日志文件的自动切割和归档管理 |
| [nginx-log-analysis.py](./python-logging/nginx-log-analysis.py) | Nginx 和系统日志分析工具，将非结构化日志转换为结构化数据 |
| [prase-IP-from-logs.py](./python-logging/prase-IP-from-logs.py) | 从日志文件中提取和分析 IP 地址信息，用于访问统计和安全分析 |
| [send-log-to-email.py](./python-logging/send-log-to-email.py) | 日志邮件通知工具，将重要日志信息通过邮件发送给管理员 |

### 配置文件操作

| 脚本路径 | 功能简介 |
|---------|---------|
| [get-config-from-yaml.py](./python-config-file-operation/get-config-from-yaml.py) | 从 YAML 配置文件中提取特定配置项，简化配置文件读取操作 |
| [json-config-management.py](./python-config-file-operation/json-config-management.py) | JSON 配置文件的读取、修改和保存操作，支持配置项的动态更新 |
| [save-system-metrics-to-json.py](./python-config-file-operation/save-system-metrics-to-json.py) | 收集系统性能指标数据并保存为 JSON 格式，便于后续分析和处理 |
| [yaml-config-management.py](./python-config-file-operation/yaml-config-management.py) | YAML 配置文件管理，演示如何安全地解析 Kubernetes 部署文件等复杂嵌套结构 |
| [yamo-config-update-in-scale.py](./python-config-file-operation/yamo-config-update-in-scale.py) | 批量更新 YAML 配置文件，适用于大规模配置文件管理场景 |

### API 开发

| 脚本路径 | 功能简介 |
|---------|---------|
| [server-health-api-client-with-logging.py](./python-api-development/server-health-api-client-with-logging.py) | 服务器健康检查 API 客户端，包含日志记录功能，用于定期获取服务器状态信息 |
| [server-health-api-server.py](./python-api-development/server-health-api-server.py) | 基于 Flask 的服务器健康检查 REST API 服务，提供 CPU、内存、磁盘使用率等系统指标 |
| [service-check-api-server.py](./python-api-development/service-check-api-server.py) | 服务管理 REST API 服务器，提供 Nginx 等系统服务的远程状态查询和重启操作 |
| [service-check-client.py](./python-api-development/service-check-client.py) | 服务检查 API 客户端，用于调用服务管理 API 进行远程服务状态监控 |

### 数据库操作

| 脚本路径 | 功能简介 |
|---------|---------|
| *目录为空* | 暂无数据库相关脚本 |

## 技术栈

- **Web 框架**: Flask (REST API 开发)
- **GUI 框架**: Tkinter (桌面应用程序)
- **系统监控**: psutil (系统资源监控)
- **容器编排**: Kubernetes Python Client
- **远程连接**: paramiko (SSH 连接)
- **配置文件**: PyYAML, JSON
- **日志处理**: 正则表达式, 文件操作
- **服务管理**: systemctl, subprocess

## 使用说明

1. 确保已安装 Python 3.x 环境
2. 根据需要安装相应的依赖包：
   ```bash
   pip install flask psutil kubernetes paramiko pyyaml
   ```
3. 根据具体脚本需求配置相关参数（如服务器地址、认证信息等）
4. 运行对应的 Python 脚本
