from django.db import models
from datetime import datetime
from collections import OrderedDict
import json


class Result(models.Model):

    class Meta:
        ordering = ['-pub_date']
    name = models.CharField(max_length=200)
    project = models.ForeignKey('Project', default=None)
    params = models.TextField(blank=True)     # 辞書をpickle化して保存
    eval_val = models.FloatField()
    solver = models.ForeignKey('Solver')
    pub_date = models.DateTimeField(default=datetime.now)
    elapsed_time = models.FloatField(default=-1.0)
    comment = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Solver(models.Model):

    class Meta:
        ordering = ['-registered_date']
    name = models.CharField(max_length=200)
    project = models.ForeignKey('Project', default=None)
    params_info = models.TextField(blank=True)
    solver_file = models.FileField(upload_to='solver', blank=True, max_length=200)
    registered_date = models.DateTimeField(default=datetime.now)
    comment = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_keys(self):
        """ 辞書形式の文字列params_infoのkeysを取得 """
        try:
            dic = json.loads(self.params_info, object_pairs_hook=OrderedDict)
        except ValueError as err:
            print("{} : {}".format(type(err), err))
            dic = {}
        except SyntaxError as err:
            print("{} : {}".format(type(err), err))
            dic = {}
        return dic.keys()

    def get_values(self):
        """ 辞書形式の文字列params_infoのvaluesを取得 """
        try:
            dic = json.loads(self.params_info, object_pairs_hook=OrderedDict)
        except ValueError as err:
            print("{} : {}".format(type(err), err))
            dic = {}
        except SyntaxError as err:
            print("{} : {}".format(type(err), err))
            dic = {}

        return dic.values()


class Project(models.Model):

    class Meta:
        ordering = ['-registered_date']
    name = models.CharField(max_length=200)
    registered_date = models.DateTimeField(default=datetime.now)
    comment = models.TextField(blank=True)

    def __str__(self):
        return self.name
