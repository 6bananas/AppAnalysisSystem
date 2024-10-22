import os.path
from collections import Counter
from .is_sex import traversal_files
from core.static_analyze import *


judge_list = []
is_yellow = ''

def get_is_yellow():
    global is_yellow
    return is_yellow


def get_judge_list():
    global judge_list
    return judge_list


def process():
    global is_yellow, judge_list
    apk_path = get_apk_path()

    app_name = ''
    version_name = ''
    version_code = ''
    package_name = ''
    sdk_version = ''
    main_activity = ''
    v1v2v3 = ''
    apk_size = 0
    component = False
    component_num = 0
    permission = False
    permission_num = 0

    list = []

    def calculate_entropy(string):
        # 统计每个字符的频率
        freq = Counter(string)
        # 总字符数
        total = len(string)
        # 计算信息熵
        entropy = -sum((count / total) * math.log2(count / total) for count in freq.values())
        return entropy

    def get_v1v2v3():
        is_v1 = 0
        is_v2 = 0
        is_v3 = 0
        with zipfile.ZipFile(apk_path, 'r') as z:
            files = z.namelist()
            for file in files:
                if file.endswith('.SF'):
                    is_v1 = 1
                    with z.open(file, 'r') as f:
                        for i in range(4):
                            if i == 3:
                                s = f.readline().strip()
                                if len(s) == 23:
                                    is_v2 = 1
                                elif len(s) == 26:
                                    is_v2 = 1
                                    is_v3 = 1
                            else:
                                f.readline()
                    break
        return str(is_v1) + str(is_v2) + str(is_v3)

    def get_aprs_num(apk):
        nonlocal component
        if apk != '':
            component = True
            a = apk.get_activities()
            p = apk.get_providers()
            r = apk.get_receivers()
            s = apk.get_services()
            return len(a) + len(p) + len(r) + len(s)
        else:
            return 0

    def get_upip_num(apk):
        nonlocal permission
        if apk != '':
            permission = True
            up = apk.get_permissions()
            ip = apk.get_uses_implied_permission_list()
            return len(up) + len(ip)
        return 0

    apk = ''
    try:
        apk = APK(apk_path)
    except Exception:
        pass
    try:
        app_name = apk.get_app_name()
    except Exception:
        pass
    try:
        version_name = str(apk.get_androidversion_name())
    except Exception:
        pass
    try:
        version_code = apk.get_androidversion_code()
    except Exception:
        pass
    try:
        package_name = apk.get_package()
    except Exception:
        pass
    try:
        sdk_version = apk.get_target_sdk_version()
    except Exception:
        pass
    try:
        main_activity = apk.get_main_activity()
    except Exception:
        pass
    try:
        v1v2v3 = get_v1v2v3()
    except Exception:
        pass
    apk_size = int(os.stat(apk_path).st_size)
    apk_size = apk_size / (1024 * 1024)
    apk_size = int(apk_size)
    try:
        component_num = get_aprs_num(apk)
    except Exception:
        pass
    try:
        permission_num = get_upip_num(apk)
    except Exception:
        pass

    # apk名称信息熵
    file_path = apk_path
    index = file_path.rfind(f'\\')
    file_path = file_path[index + 1:]
    index = file_path.find('.apk')
    file_name = file_path[0:index]
    entropy = calculate_entropy(file_name)
    if entropy == -0.0:
        list.append('-1')
    else:
        list.append(str(int(entropy)))

    if app_name == '':
        list.append('0')
    else:
        list.append('1')

    if version_name == '':
        list.append('-1')
    else:
        s = ''
        for i in version_name:
            o = ord(i)
            if (o >= 48 and o <= 57) or i == '.':
                s += i
        point = s.find('.')
        v = ''
        if s == '':
            list.append('-1')
        else:
            if point == -1:
                v = s
            else:
                v = s[0:point]
            list.append(v)

    if version_code == '':
        list.append('-1')
    else:
        list.append(version_code)

    if package_name == '':
        list.append('-1')
    else:
        entro = calculate_entropy(package_name)
        list.append(str(int(entro)))

    if sdk_version == '':
        list.append('0')
    else:
        list.append('1')

    if main_activity == '':
        list.append('0')
    else:
        list.append('1')

    if v1v2v3 == '000':
        list.append('0')
    elif v1v2v3 == '001':
        list.append('1')
    elif v1v2v3 == '010':
        list.append('2')
    elif v1v2v3 == '011':
        list.append('3')
    elif v1v2v3 == '100':
        list.append('4')
    elif v1v2v3 == '101':
        list.append('5')
    elif v1v2v3 == '110':
        list.append('6')
    elif v1v2v3 == '111':
        list.append('7')

    list.append(str(apk_size))

    if component == False:
        list.append('-1')
    else:
        list.append(str(component_num))

    if permission == False:
        list.append('-1')
    else:
        list.append(str(permission_num))

    file_name = get_image_file_path()
    yellow = traversal_files(file_name)
    is_yellow = yellow
    list.append(yellow)
    judge_list = list


