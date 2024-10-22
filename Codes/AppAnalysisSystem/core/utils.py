import os
import shutil

# 删除文件/文件夹
def delete_files(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)

# 清除缓存
def delete_cache():
    delete_files('../AppAnalysisSystem/messages/images')
    delete_files('../AppAnalysisSystem/messages/output')
    delete_files('../AppAnalysisSystem/messages/temp')
    delete_files('./messages/cert.txt')
    delete_files('./messages/md5.txt')
    delete_files('./messages/static_sites.txt')
    delete_files('./messages/dynamic_sites.txt')
    delete_files('./messages/core_sites.txt')
    delete_files('./messages/monkey.txt')
    delete_files('./messages/log.txt')
