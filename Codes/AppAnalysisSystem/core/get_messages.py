import os.path
from MysqlModel.views import *
from core.static_analyze import *
from core.dynamic_analyze import dynamic, set_dynamic_flag
from core.get_core_sites import get_site_list
from model.generate_vector import process, get_is_yellow
from model.judge.judge_type import get_judge_result
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# 分析信息
datas = ''
# APK采集是否成功，用于决定是否调用分析函数
apk_flag = False
permission_data = ''
channel_layer = get_channel_layer()


def get_apk_flag():
    global apk_flag
    return apk_flag


def set_apk_flag(flag):
    global apk_flag
    apk_flag = flag


def get_datas():
    global datas
    return datas


def set_datas(data):
    global datas
    datas = data


def get_permission_data():
    global permission_data
    return permission_data


def set_permisson_data(p):
    global permission_data
    permission_data = p


# 向前端推送消息
def websocket_send(msg):
    global channel_layer
    async_to_sync(channel_layer.group_send)(
        'progress_group',
        {
            'type': 'send_progress_update',
            'progress': msg,
        }
    )

# 调用分析函数，获得分析信息
def get_msg():
    if get_apk() is None:
        websocket_send('报错')
        set_apk_flag(False)
    else:
        websocket_send('准备分析')
        md5 = get_md5()
        app_name = get_app_name()
        package_name = get_package_name()
        is_in_while = is_in_whitelist(md5, app_name, package_name)
        is_in_gamble = is_in_gamblelist(md5, app_name, package_name)
        is_in_sex = is_in_sexlist(md5, app_name, package_name)
        is_in_scam = is_in_scamlist(md5, app_name, package_name)
        is_in_black = is_in_blacklist(md5, app_name, package_name)
        if is_in_while is True:
            websocket_send('白名单')
        elif is_in_gamble is True:
            websocket_send('涉赌名单')
        elif is_in_sex is True:
            websocket_send('涉黄名单')
        elif is_in_scam is True:
            websocket_send('涉诈名单')
        elif is_in_black is True:
            websocket_send('黑灰产名单')
        # 非白名单APP才进行分析
        if is_in_while is False:
            websocket_send('正在解析APK信息')
            print('正在解析APK信息')
            # 变量含义可对应前端展示信息知晓
            version_name = get_version_name()
            version_code = get_version_code()
            sdk_version = get_sdk_version()
            main_activity = get_main_activity()
            activities = get_activities()
            providers = get_providers()
            receivers = get_receivers()
            services = get_services()
            apk_size = get_apk_size()
            permissions = get_permission()
            set_permisson_data(permissions)
            websocket_send('正在解析签名证书')
            print('正在解析签名证书')
            v1v2v3 = get_v1_v2_v3()
            get_certificate()
            writer = ''
            owner = ''
            issuer = ''
            serialize = ''
            valid_time = ''
            cert_md5 = ''
            cert_sha1 = ''
            cert_sha256 = ''
            algro = ''
            rsa = ''
            cert_version = ''
            with open('AppAnalysisSystem/messages/cert.txt', 'r') as f:
                while True:
                    line = f.readline()
                    if not line:
                        break
                    if line.find('所有者') != -1:
                        owner = line[5:-1]
                        index = line.find('=')
                        index += 1
                        while (line[index] >= 'A' and line[index] <= 'Z') or (
                                line[index] >= 'a' and line[index] <= 'z') or (
                                line[index] >= '0' and line[index] <= '9') or line[index] == '.':
                            writer += line[index]
                            index += 1
                    if line.find('发布者') != -1:
                        issuer = line[5:-1]
                    if line.find('序列号') != -1:
                        serialize = line[5:-1]
                    if line.find('有效期') != -1:
                        valid_time = line[5:-1]
                    if line.find('生效时间') != -1:
                        valid_time = line[:-1]
                    if line.find('MD5') != -1:
                        lst = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
                        index = line.find(':')
                        while(line[index] not in lst):
                            index += 1
                        cert_md5 = line[index:-1]
                    if line.find('SHA1:') != -1:
                        cert_sha1 = line[8:-1]
                    if line.find('SHA256:') != -1:
                        cert_sha256 = line[10:-1]
                    if line.find('签名算法名称') != -1:
                        algro = line[8:-1]
                    if line.find('主体公共密钥算法') != -1:
                        rsa = line[10:-1]
                    if line.find('版本') != -1:
                        cert_version = line[4:-1]
            websocket_send('正在获取APK图片资源')
            print('正在获取APK图片资源')
            get_images()
            websocket_send('正在扫描APK文件')
            print('正在扫描APK文件')
            get_static_sites()
            websocket_send('正在进行动态分析，预计需要30秒')
            print('正在进行动态分析，预计需要30秒')
            dynamic()
            websocket_send('正在解析通联地址，请耐心等待')
            print('正在解析通联地址，请耐心等待')
            site_list = get_site_list()
            # 所有分析信息
            json_data = {}
            # APK元信息
            info_dict = {}
            info_dict["appname"] = app_name
            apk_name = os.path.basename(get_apk_path())
            info_dict["apkname"] = apk_name
            info_dict["writer"] = writer
            info_dict["vname"] = version_name
            info_dict["vcode"] = version_code
            info_dict["apksize"] = apk_size
            info_dict["md5"] = md5
            info_dict["packname"] = package_name
            info_dict["sdk"] = sdk_version
            cert_dict = {}
            cert_dict["v1"] = v1v2v3[0]
            cert_dict["v2"] = v1v2v3[1]
            cert_dict["v3"] = v1v2v3[2]
            cert_dict["owner"] = owner
            cert_dict["issuer"] = issuer
            cert_dict["serialize"] = serialize
            cert_dict["time"] = valid_time
            cert_dict["md5"] = cert_md5
            cert_dict["sha1"] = cert_sha1
            cert_dict["sha256"] = cert_sha256
            cert_dict["algro"] = algro
            cert_dict["rsa"] = rsa
            cert_dict["version"] = cert_version
            activity_list = []
            for a in activities:
                activity_list.append({"activity": a})
            provider_list = []
            for p in providers:
                provider_list.append({"provider": p})
            receiver_list = []
            for r in receivers:
                receiver_list.append({"receiver": r})
            service_list = []
            for s in services:
                service_list.append({"service": s})
            json_data["info"] = info_dict
            json_data["cert"] = cert_dict
            json_data["activity"] = activity_list
            json_data["provider"] = provider_list
            json_data["receiver"] = receiver_list
            json_data["service"] = service_list
            json_data["mainActivity"] = main_activity
            json_data["permission"] = permissions
            json_data["link"] = site_list
            apkpath = get_apk_path()
            json_data["apklong"] = len(os.path.basename(apkpath))
            websocket_send('正在生成特征向量')
            print('正在生成特征向量')
            process()
            websocket_send('正在研判，请耐心等待')
            print('正在研判，请耐心等待')
            judge_result = get_judge_result()
            print(judge_result)
            json_data["judge"] = judge_result
            json_data["image"] = get_is_yellow()
            websocket_send('分析研判完成')
            print('分析研判完成')
            set_datas(json_data)
            set_dynamic_flag(False)
            # 无待分析APK
            set_apk_flag(False)
