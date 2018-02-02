#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/1 下午6:26
# @Author  : guowei
# @Site    : 
# @File    : test.py
# @Software: PyCharm

from etherscan.accounts import Account
import json

with open('../api_key.json', mode='r') as key_file:
    key = json.loads(key_file.read())['key']

#  address = ['0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a', '0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a']
address = '0x006922CF75094708c691d06818034d89aeB23ca0'

api = Account(address=address, api_key=key)
transactions = api.get_all_transactions(offset=100, sort='desc', internal=False)


print(transactions)