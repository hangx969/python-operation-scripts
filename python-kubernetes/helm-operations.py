import subprocess, yaml, os

def helm_repo_add(repo, url):
    try:
        result = subprocess.run(f'helm repo add {repo} {url}', shell=True, encoding='utf-8', capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Helm repo {repo} is added.")

    except subprocess.CalledProcessError as e:
        print(f"Command Execution failed: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")

def helm_repo_update(repo):
    try:
        result = subprocess.run(f'helm repo update {repo}', shell=True, capture_output=True, encoding='utf-8', text=True)
        if result.returncode == 0:
            print(f"Helm repo {repo} is updated.")

    except subprocess.CalledProcessError as e:
        print(f"Command Execution failed: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")

def helm_chart_pull(repo, chart_name, version):
    try:
        result = subprocess.run(f'helm pull {repo}/{chart_name} --version {version}', shell=True, capture_output=True, encoding='utf-8', text=True)
        if result.returncode == 0:
            print(f"Helm chart {chart_name} is pulled.")

    except subprocess.CalledProcessError as e:
        print(f"Command Execution failed: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")


def helm_login_harbor(harbor_url):
    try:
        result = subprocess.run(f"helm registry login {harbor_url} --username 'admin' --password 'Harbor12345' --insecure", shell=True, capture_output=True, encoding='utf-8', text=True)
        if result.returncode == 0:
            print(f"Harbor {harbor_url} login successfully.")

    except subprocess.CalledProcessError as e:
        print(f"Command Execution failed: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")


def helm_push_harbor(harbor_url, chart_file, repo_name):
    try:
        result = subprocess.run(f"helm push {chart_file} oci://{harbor_url}/platform-tools-local/{repo_name} --insecure-skip-tls-verify", shell=True, capture_output=True, encoding='utf-8', text=True)
        if result.returncode == 0:
            print(f"Harbor {harbor_url} login successfully.")

    except subprocess.CalledProcessError as e:
        print(f"Command Execution failed: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    try:
        charts_file = os.path.join(os.path.dirname(__file__),'helm-charts-lists.yaml')
        harbor_url = "harbor.hanxux.local"
        with open(charts_file, 'r') as f:
            charts = yaml.safe_load(f)
            for chart_name, chart_info in charts.items():
                helm_repo_add(chart_info['repoName'], chart_info['repoURL'])
                helm_repo_update(chart_info['repoName'])

                chart_dir = r'D:\InstallationPackages\helm-charts'
                if not os.path.exists(chart_dir):
                    os.makedirs(chart_dir)
                os.chdir(chart_dir)
                helm_chart_pull(chart_info['repoName'], chart_name, chart_info['chartVersion'])
                # TODO: Add logic for pushing chart to harbor

    except Exception as e:
        print(f"Error: {str(e)}")

