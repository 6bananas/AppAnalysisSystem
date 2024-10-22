from .models import *

def is_in_whitelist(md5, appname, packagename):
    try:
        result = WhiteList.objects.filter(
            md5=md5,
            appname=appname,
            packagename=packagename
        ).first()
        return result is not None
    except Exception as e:
        print(f'query whitelist unexpected error: {e}')
        return False

def is_in_gamblelist(md5, appname, packagename):
    try:
        result = GambleList.objects.filter(
            md5=md5,
            appname=appname,
            packagename=packagename
        ).first()
        return result is not None
    except Exception as e:
        print(f'query gamblelist unexpected error: {e}')
        return False

def is_in_sexlist(md5, appname, packagename):
    try:
        result = SexList.objects.filter(
            md5=md5,
            appname=appname,
            packagename=packagename
        ).first()
        return result is not None
    except Exception as e:
        print(f'query sexlist unexpected error: {e}')
        return False

def is_in_scamlist(md5, appname, packagename):
    try:
        result = ScamList.objects.filter(
            md5=md5,
            appname=appname,
            packagename=packagename
        ).first()
        return result is not None
    except Exception as e:
        print(f'query scamlist unexpected error: {e}')
        return False

def is_in_blacklist(md5, appname, packagename):
    try:
        result = BlackList.objects.filter(
            md5=md5,
            appname=appname,
            packagename=packagename
        ).first()
        return result is not None
    except Exception as e:
        print(f'query blacklist unexpected error: {e}')
        return False

def query_permission(name):
    try:
        result = Permission.objects.filter(name=name).first()
        state = '未知'
        description = ''
        if result:
            description = result.description
            level = result.level
            if level == '0':
                state = '正常'
            elif level == '1':
                state = '危险'
        return [description, state]
    except Exception as e:
        print(f'query permission unexpected error: {e}')
        return [None, '未知']
