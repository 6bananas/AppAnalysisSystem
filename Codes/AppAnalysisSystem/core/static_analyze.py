import zipfile
import os
import platform
import re
import math
import time
import random
from androguard.core.bytecodes.apk import APK
from PIL import Image
from MysqlModel.views import query_permission


apk_path = None
apk = None # APK对象
random_name = None # 随机命名，用于APK图片存储文件夹
icon_path = 'statics/images/none.png'
mime_type = 'image/png'
image_file_path = None


def get_apk():
    global apk, icon_path
    try:
        apk = APK(apk_path)
        set_random_name()
    except Exception as e:
        print(f'static analyze error: {e}')
    finally:
        return apk


def get_apk_path():
    global apk_path
    return apk_path


def set_apk_path(path):
    global apk_path
    apk_path = path


def get_image_file_path():
    global image_file_path
    return image_file_path


def set_image_file_path(path):
    global image_file_path
    image_file_path = path


def set_random_name():
    global random_name
    random.seed(int(time.time()))
    random_name = str(random.getrandbits(64))


def get_icon_path():
    global icon_path
    return icon_path


def set_icon_path(path):
    global icon_path
    icon_path = path


def get_mime_type():
    global mime_type
    return mime_type


def set_mime_type(mimetype):
    global mime_type
    mime_type = mimetype


def get_app_name():
    global apk
    if apk is not None:
        try:
            app_name = apk.get_app_name()
            return app_name
        except Exception as e:
            print(f'static analyze error: {e}')
            return ''
    return ''


def get_package_name():
    global apk
    if apk is not None:
        try:
            package_name = apk.get_package()
            return package_name
        except Exception as e:
            print(f'static analyze error: {e}')
            return ''
    return ''


def get_version_name():
    global apk
    if apk is not None:
        try:
            version_name = apk.get_androidversion_name()
            return version_name
        except Exception as e:
            print(f'static analyze error: {e}')
            return ''
    return ''


def get_version_code():
    global apk
    if apk is not None:
        try:
            version_code = apk.get_androidversion_code()
            return version_code
        except Exception as e:
            print(f'static analyze error: {e}')
            return ''
    return ''


def get_sdk_version():
    global apk
    if apk is not None:
        try:
            sdk_version = apk.get_target_sdk_version()
            return sdk_version
        except Exception as e:
            print(f'static analyze error: {e}')
            return ''
    return ''


def get_main_activity():
    global apk
    if apk is not None:
        try:
            main_activity = apk.get_main_activity()
            return main_activity
        except Exception as e:
            print(f'static analyze error: {e}')
            return ''
    return ''


def get_activities():
    global apk
    if apk is not None:
        try:
            activities = apk.get_activities()
            return activities
        except Exception as e:
            print(f'static analyze error: {e}')
            return ''
    return ''


def get_providers():
    global apk
    if apk is not None:
        try:
            providers = apk.get_providers()
            return providers
        except Exception as e:
            print(f'static analyze error: {e}')
            return ''
    return ''


def get_receivers():
    global apk
    if apk is not None:
        try:
            receivers = apk.get_receivers()
            return receivers
        except Exception as e:
            print(f'static analyze error: {e}')
            return ''
    return ''


def get_services():
    global apk
    if apk is not None:
        try:
            services = apk.get_services()
            return services
        except Exception as e:
            print(f'static analyze error: {e}')
            return ''
    return ''


def get_permission():
    global apk
    if apk is not None:
        try:
            permissions = apk.get_permissions()
            implied_permissions = apk.get_uses_implied_permission_list()
            result = []
            for i in implied_permissions:
                for j in i:
                    if j is not None:
                        permissions.append(j)
            for permission in permissions:
                index = permission.rfind('.')
                permission = permission[index+1:]
                p = query_permission(permission)
                item = {"name": permission, "description": p[0], "level": p[1]}
                result.append(item)
            return result
        except Exception as e:
            print(f'static analyze error: {e}')
            return ''
    return ''


def get_apk_size():
    global apk_path
    byte_num = os.stat(apk_path).st_size
    if byte_num == 0:
        return '0MB'
    size_name = ('B', 'KB', 'MB', 'GB')
    i = int(math.floor(math.log(byte_num, 1024)))
    p = math.pow(1024, i)
    size = round(byte_num / p, 2)
    return f'{size}{size_name[i]}'


def get_md5():
    global apk_path
    os_type = platform.system()
    if os_type == 'Windows':
        os.system(f'certutil -hashfile {apk_path} MD5 > AppAnalysisSystem/messages/md5.txt')
        with open('AppAnalysisSystem/messages/md5.txt', 'r') as f:
            for i in range(2):
                if i == 1:
                    return f.readline().strip()
                else:
                    f.readline()


def get_v1_v2_v3():
    global apk_path
    is_v1 = False
    is_v2 = False
    is_v3 = False
    try:
        with zipfile.ZipFile(apk_path, 'r') as z:
            files = z.namelist()
            for file in files:
                if file.endswith('.SF'):
                    is_v1 = True
                    with z.open(file, 'r') as f:
                        for i in range(4):
                            if i == 3:
                                s = f.readline().strip()
                                if len(s) == 23:
                                    is_v2 = True
                                elif len(s) == 26:
                                    is_v2 = True
                                    is_v3 = True
                            else:
                                f.readline()
    except Exception as e:
        print(f'static analyze error: {e}')

    return [is_v1, is_v2, is_v3]


def get_certificate():
    global apk_path
    os.system(f'keytool -printcert -jarfile {apk_path} > c.txt')
    content = ''
    with open('c.txt', 'r') as c:
        for i in range(28):
            s = c.readline()
            if s.find('扩展') != -1:
                break
            if s != '\n':
                content += s
    with open('AppAnalysisSystem/messages/cert.txt', 'w') as cert:
        cert.write(content)
    os.system('del c.txt')


def get_images():
    global apk, apk_path, random_name
    mime_types = {
        'png': 'image/png',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'gif': 'image/gif',
        'bmp': 'image/bmp',
        'webp': 'image/webp'
    }
    if apk is not None:
        output_dir = f'AppAnalysisSystem/messages/images/{random_name}/img'
        set_image_file_path(output_dir)
        os.makedirs(output_dir)
        try:
            icon = apk.get_app_icon()
        except Exception:
            pass
        with zipfile.ZipFile(apk_path, 'r') as z:
            images = [file for file in z.namelist() if
                      file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'))]
            for image in images:
                try:
                    with z.open(image) as image_data:
                        img = Image.open(image_data)
                        img_path = os.path.join(output_dir, os.path.basename(image))
                        if image == icon:
                            img_path = os.path.basename(image)
                            file_name, suffix = os.path.splitext(img_path)
                            img_path = f'AppAnalysisSystem/messages/images/{random_name}/icon{suffix}'
                            path_to_icon = f'AppAnalysisSystem/messages/images/{random_name}/icon{suffix}'
                            set_icon_path(path_to_icon)
                            img.save(img_path)
                            set_mime_type(mime_types[suffix])
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        img.save(img_path)
                except Exception as e:
                    print(f"skip {image}: {e}")


def get_static_sites():
    global apk_path, random_name
    os.chdir('AppAnalysisSystem/apktool')
    output_file = os.path.join('..', 'messages', 'output', random_name)
    basename = os.path.basename(apk_path)
    os.system(f'apktool d ../apk/{basename} -o {output_file}')
    print('调试信息：已结束apktool')
    url_pattern = re.compile(r'https?://[a-zA-Z0-9\./_&=@$%?~#-]*')
    sites = set()
    for root, dirs, files in os.walk(output_file):
        for file in files:
            file_path = os.path.join(root, file)
            if not os.path.exists(file_path):
                continue
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                contents = f.read()
                url = url_pattern.findall(contents)
                sites.update(url)
    os.chdir('../../')
    with open('AppAnalysisSystem/messages/static_sites.txt', 'w') as f:
        for i in sorted(sites):
            f.write(i + '\n')

    print('调试信息：已退出get_static_sites')





