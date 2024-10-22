import os, requests, ahocorasick
from .dynamic_analyze import get_dynamic_flag

requests.packages.urllib3.disable_warnings()

whitelist = [
    '%',
    'fb.me',
    'momentjs.',
    'android',
    '.org',
    'font',
    'google',
    'github',
    'git',
    'gitee',
    'npms.',
    'bmob.',
    'adobe',
    'apache',
    'jpush',
    'localhost',
    'cloud',
    'qq.',
    'umeng',
    'umsns',
    'baidu',
    'e4asoft',
    'iec.ch',
    'esotericsoftware',
    'youtube',
    'apple',
    'flutter',
    'wikipedia',
    'microsoft',
    'verisign',
    'ldmnq',
    'cdn',
    'api',
    'qqmail',
    'qmail',
    'example',
    'office',
    'outlook',
    'live',
    '.jpg',
    '.png',
    '.gif',
    '.webp',
    '.bmp',
    '127.0.0.1',
    'java',
    'app',
    'sentry',
    'domain',
    'taobao',
    'alipay',
    'twitter',
    'facebook',
    'wechat',
    'opensourcecache',
    'bootstrap',
    'element',
    'jquery',
    'lodash',
    'code',
    'meiqia',
    'amazon',
    'xiaomi'
]

def build_aho_corasick_automaton(patterns):
    automaton = ahocorasick.Automaton()
    for idx, pattern in enumerate(patterns):
        automaton.add_word(pattern, (idx, pattern))
    automaton.make_automaton()
    return automaton

def get_site_list():
    global whitelist
    whitelist_automaton = build_aho_corasick_automaton(whitelist)
    if get_dynamic_flag() is True:
        files = ['AppAnalysisSystem/messages/dynamic_sites.txt', 'AppAnalysisSystem/messages/static_sites.txt']
    else:
        files = ['AppAnalysisSystem/messages/static_sites.txt']
    urls = []

    for file in files:
        if os.path.exists(file):
            with open(file, 'r') as f:
                for site in f:
                    site = site.strip()
                    if site.endswith('...'):
                        site = site[:-3]
                    if site.endswith('.com/'):
                        site = site[:-1]
                    flag = True
                    if site.endswith('?'):
                        flag = False
                    elif site == 'http://':
                        flag = False
                    elif site == 'https://':
                        flag = False
                    elif site == 'http://www.':
                        flag = False
                    elif site == 'https://www.':
                        flag = False
                    elif site in urls:
                        flag = False
                    else:
                        for end_index, (idx, pattern) in whitelist_automaton.iter(site):
                            flag = False
                            break
                    if flag and site not in urls:
                        urls.append(site)

    with open('AppAnalysisSystem/messages/core_sites.txt', 'w') as cs:
        cs.write("\n".join(urls))

    site_list = []

    with open('AppAnalysisSystem/messages/core_sites.txt', 'r') as file:
        for line in file:
            line = line.strip()
            item = {"url": line}
            try:
                try:
                    response = requests.get(line, verify=False, proxies={"http": None, "https": None}, timeout=3)
                except requests.exceptions.Timeout:
                    response = requests.get(line, verify=False, proxies={"http": None, "https": None}, timeout=6)
                item["state"] = response.status_code
            except Exception:
                item["state"] = "error"
            finally:
                site_list.append(item)

    return site_list
