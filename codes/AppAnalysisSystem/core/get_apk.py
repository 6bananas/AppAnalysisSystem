import cv2
import requests
import os
import re
from pyzbar.pyzbar import decode
from .static_analyze import set_apk_path
from concurrent.futures import ThreadPoolExecutor


# 分块下载
def download_chunk(url, start, end, chunk_num):
    headers = {'Range': f'bytes={start}-{end}'}
    response = requests.get(url, headers=headers, stream=True)
    chunk_file = f"chunk_{chunk_num}"
    with open(chunk_file, 'wb') as f:
        f.write(response.content)
    return chunk_file


# 下载块合并
def merge_chunks(chunk_files, output_path):
    with open(output_path, 'wb') as output_file:
        for chunk_file in chunk_files:
            with open(chunk_file, 'rb') as f:
                output_file.write(f.read())
            os.remove(chunk_file)


def is_valid_link(download_link):
    # 如果链接不包含.apk后缀，再通过魔术数字判断
    response = requests.get(download_link, stream=True, timeout=2)
    response.raise_for_status()  # 如果请求不成功，会抛出异常
    magic_number = b'\x50\x4B\x03\x04'  # APK文件的魔术数字
    # 读取文件前几个字节并与APK文件的魔术数字进行比较
    first_bytes = response.raw.read(len(magic_number))
    response.close()
    if first_bytes == magic_number:
        return [True, download_link]
    else:
        response = requests.get(download_link)
        html_content = response.text
        pattern = r'href="([^"]+\.apk)"'
        matches = re.search(pattern, html_content).group()
        index = matches.find('=')
        if matches.find('.apk') != -1:
            suffix = matches[index + 2:-1]
            link = download_link + suffix
            return [True, link]
        else:
            return [False, 'no link']


# 普通下载
def download_from_link_slow(download_link):
    try:
        apk_file = requests.get(download_link)
        apk_path = 'AppAnalysisSystem/apk/app.apk'
        set_apk_path(apk_path)
        with open(apk_path, 'wb') as f:
            f.write(apk_file.content)
        if os.path.exists(apk_path):
            print('download apk success')
            return 1
    except Exception as e:
        print(f'download apk error: {e}')
        return 0


# 多线程下载
def download_from_link_fast(download_link, num_threads=5):
    try:
        response = requests.head(download_link)
        file_size = int(response.headers['Content-Length'])
        chunk_size = file_size // num_threads
        chunk_files = []
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = []
            for i in range(num_threads):
                start = i * chunk_size
                end = start + chunk_size - 1 if i < num_threads - 1 else file_size - 1
                futures.append(executor.submit(download_chunk, download_link, start, end, i))
            for future in futures:
                chunk_files.append(future.result())
        index = download_link.rfind('/')
        apk_path = 'AppAnalysisSystem/apk/' + download_link[index + 1:]
        set_apk_path(apk_path)
        merge_chunks(chunk_files, apk_path)
        if os.path.exists(apk_path):
            print('download apk success')
            return 1
    except Exception as e:
        print(f'download apk error: {e}')
        return 0


def download_from_qr_code(image_path):
    img = cv2.imread(image_path)
    qr_codes = decode(img)
    if qr_codes:
        qr_data = qr_codes[0].data.decode('utf-8')
        if qr_data.endswith('.apk'):
            return download_from_link_fast(qr_data)
        else:
            return download_from_link_slow(qr_data)
    else:
        print('decode qr code error')
        return 0
