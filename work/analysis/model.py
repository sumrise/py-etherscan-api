#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/6 下午5:39
# @Author  : sumrise
# @Site    : 
# @File    : model.py
# @Software: PyCharm


class Transaction:
    account = ''
    to = ''
    value = ''
    date = ''

    def __init__(self, account, to, value, date):
        self.account = account
        self.to = to
        self.value = value
        self.date = date

    def as_json(self):
        return dict(
            date=self.date, address=self.account, to=self.to, value=self.value)
