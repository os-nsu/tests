import subprocess

def start_proxy(project_dir, proxy_bin_name):
	proxy = subprocess.run([f"{proxy_bin_name}"], cwd=project_dir, check=True)
	assert proxy.returncode == 0, "Proxy exit code is 0"
	return proxy
