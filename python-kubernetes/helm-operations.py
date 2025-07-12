"""
Helm Charts 批量管理和 Harbor 推送工具

功能描述:
    该脚本用于自动化管理 Helm Charts 的完整生命周期，包括仓库管理、
    Chart 下载和推送到私有 Harbor 仓库。主要实现以下功能：

    1. Helm 仓库管理
       - 检查仓库是否已添加，避免重复操作
       - 批量添加 Helm 仓库
       - 更新仓库索引

    2. Chart 包管理
       - 批量下载指定版本的 Helm Charts
       - 检查本地文件是否存在，避免重复下载
       - 支持多种 Chart 格式和版本

    3. Harbor 集成
       - 登录私有 Harbor 仓库（支持 PowerShell 环境）
       - 推送 Chart 包到 Harbor 的 OCI 仓库
       - 支持不安全连接和自签名证书

配置文件:
    - helm-charts-lists.yaml: 包含所有要管理的 Charts 信息
    - 支持 repoName, repoURL, chartVersion, chartFileName 字段
"""

import subprocess, yaml, os

def is_helm_repo_added(repo):
    try:
        result = subprocess.run(f"helm repo list", shell=True, encoding='utf-8', capture_output=True, text=True, errors='ignore')
        if result.returncode == 0:
            if repo in result.stdout:
                print(f"Helm repo {repo} has been added, skipping.")
                return True
            else:
                print(f"Helm repo {repo} has not been added yet.")
                return False
    except subprocess.CalledProcessError as e:
        print(f"Command Execution failed: {str(e)}")
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def helm_repo_add(repo, url):
    try:
        result = subprocess.run(f'helm repo add {repo} {url}', shell=True, encoding='utf-8', capture_output=True, text=True, errors='ignore')
        if result.returncode == 0:
            print(f"Helm repo {repo} is added.")
        else:
            print(f"Error adding repo {repo}: {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Command Execution failed: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")

def helm_repo_update(repo):
    try:
        result = subprocess.run(f'helm repo update {repo}', shell=True, capture_output=True, encoding='utf-8', text=True, errors='ignore')
        if result.returncode == 0:
            print(f"Helm repo {repo} is updated.")
        else:
            print(f"Error updating repo {repo}: {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Command Execution failed: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")

def helm_chart_pull(repo, chart_name, version):
    try:
        result = subprocess.run(f'helm pull {repo}/{chart_name} --version {version}', shell=True, capture_output=True, encoding='utf-8', text=True, errors='ignore')
        if result.returncode == 0:
            print(f"Helm chart {chart_name} is pulled.")
        else:
            print(f"Error pulling chart {chart_name}: {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Command Execution failed: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")


# def helm_login_harbor(harbor_url):
#     try:
#         result = subprocess.run(['helm', 'registry', 'login', harbor_url, '--username', "'admin'", '--password', "'Harbor12345'", '--insecure'], capture_output=True, encoding='utf-8', text=True)
#         if result.returncode == 0:
#             print(f"Harbor {harbor_url} login successfully.")
#         else:
#             print(result.stderr)
#     except subprocess.CalledProcessError as e:
#         print(f"Command Execution failed: {str(e)}")
#     except Exception as e:
#         print(f"Error: {str(e)}")

def helm_login_harbor_powershell(harbor_url, username="admin", password="Harbor12345"):
    """使用 PowerShell 直接执行，完全模拟手动执行环境"""
    try:
        # 构造 PowerShell 脚本
        ps_script = f"""
        $ErrorActionPreference = "Stop"
        helm registry login {harbor_url} --username '{username}' --password '{password}' --insecure
        if ($LASTEXITCODE -eq 0) {{
            Write-Host "SUCCESS: Login completed"
        }} else {{
            Write-Error "FAILED: Login failed with exit code $LASTEXITCODE"
            exit $LASTEXITCODE
        }}
        """

        # 执行 PowerShell 脚本
        result = subprocess.run(
            ['powershell', '-ExecutionPolicy', 'Bypass', '-Command', ps_script],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=60
        )

        print(f"PowerShell output: {result.stdout}")
        if result.stderr:
            print(f"PowerShell error: {result.stderr}")

        if result.returncode == 0:
            print(f"Harbor {harbor_url} login successfully via PowerShell.")
            return True
        else:
            print(f"PowerShell loging failed: {result.returncode}")
            return False

    except subprocess.TimeoutExpired:
        print("PowerShell timeout")
        return False
    except Exception as e:
        print(f"PowerShell error: {str(e)}")
        return False


def helm_push_harbor(harbor_url, chart_file, repo_name):
    try:
        result = subprocess.run(f"helm push {chart_file} oci://{harbor_url}/platform-tools-local/{repo_name} --insecure-skip-tls-verify", shell=True, capture_output=True, encoding='utf-8', text=True, errors='ignore')
        if result.returncode == 0:
            print(f"Helm chart {chart_file} pushed successfully.")
        else:
            print(f"Error pushing chart {chart_file}: {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Command Execution failed: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    try:
        # 登录harbor
        harbor_url = "harbor.hanxux.local"
        helm_login_harbor_powershell(harbor_url)

        charts_info_yaml = os.path.join(os.path.dirname(__file__),'helm-charts-lists.yaml')

        chart_dir = r'D:\InstallationPackages\helm-charts'
        # 判断路径是否存在，不存在则创建
        if not os.path.exists(chart_dir):
            os.makedirs(chart_dir)

        with open(charts_info_yaml, 'r', encoding='utf-8') as f:
            # 加载同级目录下的charts信息yaml文件
            charts = yaml.safe_load(f)
            for chart_name, chart_info in charts.items():
                # 判断helm repo是否已经存在
                if not is_helm_repo_added(chart_info['repoName']):
                    # repo不存在，则添加helm repo并更新
                    helm_repo_add(chart_info['repoName'], chart_info['repoURL'])
                    helm_repo_update(chart_info['repoName'])

                # 切换到chart目录
                os.chdir(chart_dir)
                # 判断chart tgz文件是否已经存在了，不存在再去拉
                if not os.path.exists(chart_info['chartFileName']):
                    # 拉取helm chart
                    helm_chart_pull(chart_info['repoName'], chart_name, chart_info['chartVersion'])

                # push到harbor
                helm_push_harbor(harbor_url, chart_info['chartFileName'], chart_info['repoName'])

    except Exception as e:
        print(f"Error: {str(e)}")

