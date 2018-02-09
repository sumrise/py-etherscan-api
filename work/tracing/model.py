#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/9 下午3:10
# @Author  : sumrise
# @Site    : 
# @File    : model.py
# @Software: PyCharm

import peewee as pw

myDB = pw.MySQLDatabase('eth_tracing', user='root', password='EPze1/ma;!8qq',
                        host='127.0.0.1', port=9527)


# todo:modify host

class MySQLModel(pw.Model):
    class Meta:
        database = myDB


class Record(MySQLModel):
    id = pw.PrimaryKeyField()
    blockNumber = pw.IntegerField()
    timeStamp = pw.IntegerField()
    hash = pw.CharField()
    account = pw.CharField()
    to = pw.CharField()
    value = pw.DoubleField()

    class Meta:
        db_table = 'record'


class Address(MySQLModel):
    id = pw.PrimaryKeyField()
    address = pw.CharField()
    name = pw.CharField()

    def as_json(self):
        return dict(
            address=self.address, name=self.name)

    def as_list_json(self):
        return dict(self.address, self.name)

    class Meta:
        db_table = 'address'


class Node:

    def __init__(self, address, name, blockNumber, timeStamp, value, level):
        self.address = address
        self.name = name
        self.blockNumber = blockNumber
        self.timeStamp = timeStamp
        self.value = value
        self.level = level
        self.children = []

    def as_json(self):
        return dict(
            address=self.address, name=self.name, value=self.value, level=self.level,
            children=[ob.as_json() for ob in self.children])


myDB.connect()
