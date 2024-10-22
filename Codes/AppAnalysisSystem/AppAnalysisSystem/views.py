import json, threading
from core.get_messages import *
from core.get_apk import *
from core.static_analyze import *
from werkzeug.utils import secure_filename
from django.http import FileResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt


# 获取APP图标
@csrf_exempt
def get_icon(request):
    icon_path = get_icon_path()
    mime_type = get_mime_type()
    print('send icon success')
    return FileResponse(open(icon_path, 'rb'), content_type=mime_type)


# 获取APP解析信息
@csrf_exempt
def get_messages(request):
    json_data = get_datas()
    print('send messages success')
    return JsonResponse({"code": 20000, "data": json_data})


# 从链接下载APK
@csrf_exempt
def download_apk_from_link(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        link = data.get('apkLink')
        lst = is_valid_link(link)
        is_v = lst[0]
        link = lst[1]
        if not is_v:
            return JsonResponse({"code": 50000, "msg": "invalid link"})
        else:
            print('valid link')
            if link.endswith('.apk'):
                result = download_from_link_fast(link)
            else:
                result = download_from_link_slow(link)
            if result == 1:
                set_apk_flag(True)
                return JsonResponse({"code": 20000, "msg": "download apk from link success"})
            else:
                return JsonResponse({"code": 50000, "msg": "download apk from link failed"})
    return JsonResponse({"code": 50000, "msg": "invalid request method"})


# 上传APK
@csrf_exempt
def save_upload_apk(request):
    if request.method == 'POST' and request.FILES:
        file = request.FILES['file']
        file_name = request.POST.get('fileName')
        try:
            fs = FileSystemStorage()
            file_path = f'AppAnalysisSystem/apk/{file_name}'
            filename = fs.save(file_path, file)
            set_apk_flag(True)
            set_apk_path(file_path)
            print('save upload apk success')
            return JsonResponse({"code": 20000, "msg": "save upload apk success"})
        except Exception as e:
            print(f'save upload apk failed: {e}')
            return JsonResponse({"code": 50000, "msg": "save upload apk failed"})
    return JsonResponse({"code": 50000, "msg": "invalid request method"})


# 从二维码下载APK
@csrf_exempt
def download_apk_from_qr(request):
    if request.method == 'POST' and request.FILES:
        file = request.FILES['avatar']
        try:
            filename = secure_filename(file.name)
            save_path = 'AppAnalysisSystem/messages/temp'
            os.makedirs(save_path, exist_ok=True)
            qr_path = os.path.join(save_path, filename)
            with open(qr_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            result = download_from_qr_code(qr_path)
            if result == 1:
                set_apk_flag(True)
                return JsonResponse({"code": 20000, "msg": "download apk from qr success"})
            else:
                return JsonResponse({"code": 50000, "msg": "download apk from qr failed"})
        except Exception as e:
            print(f'download apk from qr failed: {e}')
            return JsonResponse({"code": 50000, "msg": "download apk from qr failed"})
    return JsonResponse({"code": 50000, "msg": "invalid request method"})


tokens = {}
# 登录
@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        if username == 'admin' and password == '111111':
            token = 'token_' + username
            tokens[token] = username
            return JsonResponse({"code": 20000, "data": {"token": token}})
        else:
            return JsonResponse({"code": 40001, "message": "invalid username or password"})
    return JsonResponse({"code": 50000, "message": "invalid request method"})


# 登出
@csrf_exempt
def logout(request):
    token = request.headers.get('X-Token')
    if token and token in tokens:
        tokens.pop(token)
        return JsonResponse({"code": 20000, "message": "logout successful"})
    else:
        return JsonResponse({"code": 40001, "message": "invalid token"})


# 获取用户基本信息
@csrf_exempt
def get_info(request):
    token = request.headers.get('X-Token')
    if token and token in tokens:
        user_info = {
            'roles': ['admin'],
            'name': 'Admin',
            'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
            'introduction': 'Hello, World!'
        }
        return JsonResponse({"code": 20000, "data": user_info})
    else:
        return JsonResponse({"code": 40001, "message": "invalid token"})


# 权限饼状图
@csrf_exempt
def get_pie_chart1(request):
    permission = get_permission_data()
    normal = 0
    dangerous = 0
    unknown = 0
    for i in permission:
        if i['level'] == '正常':
            normal += 1
        elif i['level'] == '危险':
            dangerous += 1
        elif i['level'] == '未知':
            unknown += 1
    data = {
        "legendData": ["Normal", "Dangerous", "Unknown"],
        "seriesData": [
            {"value": dangerous, "name": "Dangerous"},
            {"value": normal, "name": "Normal"},
            {"value": unknown, "name": "Unknown"}
        ]
    }
    return JsonResponse(data)


# 组件柱状图
@csrf_exempt
def get_bar_chart(request):
    activity = get_activities()
    provide = get_providers()
    receive = get_receivers()
    service = get_services()
    barchart_data = [
        len(activity),
        len(provide),
        len(receive),
        len(service)
    ]
    data = {
        "categories": ["Activity", "Provide", "Receive", "Service"],
        "pageAData": barchart_data,
        "pageBData": [],
        "pageCData": []
    }
    return JsonResponse(data)

# 开机自启动，监听是否有待分析APK，有则执行后续步骤
stop_event = threading.Event()

def handle_get_msg():
    while not stop_event.is_set():
        if get_apk_flag() is True:
            get_msg()

threading.Thread(target=handle_get_msg, args=()).start()