import os
import subprocess

# 获取当前文件的绝对路径
current_file_path = os.path.abspath(__file__)

# 获取当前文件的目录
current_directory = os.path.dirname(current_file_path)
working_directory = os.path.dirname(current_file_path)
# 改变当前工作目录
os.chdir(current_directory)

def update_repos(root_dir):
    """遍历root_dir下的所有git仓库，并更新它们到最新版本"""
    # 遍历root_dir下的所有目录
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 如果这个目录是一个git仓库
        if '.git' in dirnames:
            print(f"Updating {dirpath}")
            # 进入这个目录
            os.chdir(dirpath)
            # 运行git pull命令
            subprocess.run(["git", "pull"])
            # 返回到root_dir
            os.chdir(root_dir)

# 更新当前目录下的所有仓库
update_repos(os.getcwd())