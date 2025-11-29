from django.db import models

class WhiteList(models.Model):
    md5 = models.CharField(max_length=32, primary_key=True, verbose_name='MD5')
    appname = models.CharField(max_length=1024, blank=True, null=True, verbose_name='APP名称')
    packagename = models.CharField(max_length=1024, blank=True, null=True, verbose_name='包名')

    class Meta:
        db_table = 'whitelist'


class GambleList(models.Model):
    md5 = models.CharField(max_length=32, primary_key=True, verbose_name='MD5')
    appname = models.CharField(max_length=1024, blank=True, null=True, verbose_name='APP名称')
    packagename = models.CharField(max_length=1024, blank=True, null=True, verbose_name='包名')

    class Meta:
        db_table = 'gamblelist'


class SexList(models.Model):
    md5 = models.CharField(max_length=32, primary_key=True, verbose_name='MD5')
    appname = models.CharField(max_length=1024, blank=True, null=True, verbose_name='APP名称')
    packagename = models.CharField(max_length=1024, blank=True, null=True, verbose_name='包名')

    class Meta:
        db_table = 'sexlist'


class ScamList(models.Model):
    md5 = models.CharField(max_length=32, primary_key=True, verbose_name='MD5')
    appname = models.CharField(max_length=1024, blank=True, null=True, verbose_name='APP名称')
    packagename = models.CharField(max_length=1024, blank=True, null=True, verbose_name='包名')

    class Meta:
        db_table = 'scamlist'


class BlackList(models.Model):
    md5 = models.CharField(max_length=32, primary_key=True, verbose_name='MD5')
    appname = models.CharField(max_length=1024, blank=True, null=True, verbose_name='APP名称')
    packagename = models.CharField(max_length=1024, blank=True, null=True, verbose_name='包名')

    class Meta:
        db_table = 'blacklist'


class Permission(models.Model):
    name = models.CharField(max_length=50, primary_key=True, verbose_name='名称')
    description = models.CharField(max_length=1024, blank=False, null=False, verbose_name='描述')
    level = models.CharField(max_length=8, blank=False, null=False, verbose_name='级别')

    class Meta:
        db_table = 'permission'
