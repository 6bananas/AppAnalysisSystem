import subprocess, threading, time, re
from .static_analyze import get_package_name, get_main_activity, get_permission, get_apk_path

package_name = None
main_activity = None
permissions = None
# 是否进行了动态分析
dynamic_flag = False


def set_dynamic_flag(f):
    global dynamic_flag
    dynamic_flag = f


def get_dynamic_flag():
    global dynamic_flag
    return dynamic_flag


def grant_permissions():
    global package_name, permissions
    for permission in permissions:
        subprocess.run(f'adb shell "pm grant {package_name} {permission}"', shell=True)


def cmd(command, stop_event):
    process = subprocess.Popen(command, shell=True)
    # 循环检测停止事件是否设置
    while not stop_event.is_set():
        time.sleep(0.1)
    # 终止进程
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()


def is_installed():
    global package_name
    result = subprocess.run(f'adb shell "pm list packages | grep {package_name}"', shell=True, stdout=subprocess.PIPE)
    return package_name in result.stdout.decode()


def get_dynamic_sites():
    url_pattern = re.compile(r'https?://[a-zA-Z0-9\./_&=@$%?~#-]*')
    sites = set()
    try:
        with open('AppAnalysisSystem/messages/monkey.txt', 'r', encoding='utf-8') as f:
            contents = f.read()
            url = url_pattern.findall(contents)
            sites.update(url)
    except UnicodeDecodeError:
        with open('AppAnalysisSystem/messages/monkey.txt', 'r', encoding='iso-8859-1') as f:
            contents = f.read()
            url = url_pattern.findall(contents)
            sites.update(url)
    try:
        with open('AppAnalysisSystem/messages/log.txt', 'r', encoding='utf-8') as f:
            contents = f.read()
            url = url_pattern.findall(contents)
            sites.update(url)
    except UnicodeDecodeError:
        with open('AppAnalysisSystem/messages/log.txt', 'r', encoding='iso-8859-1') as f:
            contents = f.read()
            url = url_pattern.findall(contents)
            sites.update(url)
    with open('AppAnalysisSystem/messages/dynamic_sites.txt', 'w', encoding='utf-8') as f:
        for i in sites:
            f.write(i+'\n')


def dynamic():
    global package_name, main_activity, permissions
    apk_path = get_apk_path()
    package_name = get_package_name()
    main_activity = get_main_activity()
    permissions = get_permission()
    if package_name == '' or main_activity == '':
        print('dynamic analyze error, because static analyze failed!')
    else:
        set_dynamic_flag(True)
        subprocess.run('adb root', shell=True)
        subprocess.run('adb shell "exit"', shell=True)

        install_command = f'adb install {apk_path}'
        log_command = f'adb logcat -c & adb shell "logcat > /data/log.txt"'

        stop_event1 = threading.Event()
        stop_event2 = threading.Event()

        thread1 = threading.Thread(target=cmd, args=(install_command, stop_event1))
        thread2 = threading.Thread(target=cmd, args=(log_command, stop_event2))

        thread1.start()
        thread2.start()

        # 确保安装成功
        is_installed_flag = False
        start_time = time.time()
        while True:
            if is_installed():
                is_installed_flag = True
                break
            # 30秒后自动退出，防止死循环
            if time.time() - start_time > 30:
                break
            # 每隔1秒检查一次
            time.sleep(1)

        if is_installed_flag:
            print('APK安装成功')
            # 授权
            grant_permissions()

            # 启动APP
            subprocess.run(f'adb shell "am start -n {package_name}/{main_activity}"', shell=True)

            # 等待APP启动成功
            time.sleep(5)
            monkey_log = '/data/monkey.txt'
            # 事件之间的延迟不能太低，不然很容易崩溃
            subprocess.run(f'adb shell "monkey -p {package_name} --ignore-crashes --throttle 100 -v 2000 | 'f'egrep \'http[s]?\' > {monkey_log}"', shell=True)

        # 设置停止事件
        stop_event1.set()
        stop_event2.set()

        # 等待线程结束
        thread1.join()
        thread2.join()

        if is_installed_flag:
            subprocess.run(f'adb pull {monkey_log} AppAnalysisSystem/messages', shell=True)
            subprocess.run(f'adb shell rm {monkey_log}', shell=True)
            subprocess.run('adb pull /data/log.txt AppAnalysisSystem/messages', shell=True)
        subprocess.run('adb shell rm /data/log.txt', shell=True)
        subprocess.run(f'adb uninstall {package_name}', shell=True)

        # 获取动态运行时的地址
        get_dynamic_sites()

