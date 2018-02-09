#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/9 下午1:47
# @Author  : sumrise
# @Site    : 
# @File    : start.py
# @Software: PyCharm
import logging
from etherscan.accounts import Account
import json

from tracing.model import Record, Address, Node

with open('../../api_key.json', mode='r') as key_file:
    key = json.loads(key_file.read())['key']

tracing_floor = 10
addressList = list(Address.select().iterator())
results = [ob.as_json() for ob in addressList]
address_map = dict()
for a in results:
    address_map[a['address']] = a['name']

fatherNode = None


# 查找某个区块开始，某个地址所有的交易记录
def find_all_transactions(address, start_block):
    records = Record.select().where(Record.account == address)
    if len(records) < 0:
        api = Account(address=address, api_key=key)
        transactions = api.get_all_transactions(start_block=start_block)
        for trans in transactions:
            count = Record.select().where(Record.hash == trans['hash']).count()
            if count <= 0:
                Record.insert(blockNumber=int(trans['blockNumber']),
                              timeStamp=int(trans['timeStamp']),
                              hash=trans['hash'], account=trans['from'], to=trans['to'],
                              value=int(trans['value']) / 10 ** 18).execute()
        records = Record.select().where(Record.account == address)

    return records


# 追踪地址 开始hash,地址，开始区块
def find_tracing(fatherNode, record):
    if fatherNode.address in address_map:
        fatherNode.name = address_map[fatherNode.address]
    else:
        transactions = find_all_transactions(record.to, record.blockNumber)
        for trans in transactions:
            if trans.hash != record.hash:
                trans.delete()

        logging.info('-------------' + fatherNode.address)
        logging.info('----start----' + transactions[0].hash)
        level = 0
        for trans in transactions:
            if trans.account == record.to:  # 发出
                if trans.value - record.value > 0.01:
                    # 记录该节点
                    childNode = Node(address=trans.account, blockNumber=trans.blockNumber, timeStamp=trans.timeStamp,
                                     value=trans.value, level=level, name='')
                    fatherNode.children.append(childNode)
                    level += 1



    print('---end---')


def search_hash(address, hash):
    records = Record.select().where(Record.hash == hash)
    if len(records) > 0:
        logging.info(records[0])
    else:
        records = find_all_transactions(address, 0)

    record = records[0]
    fatherNode = Node(address=address, blockNumber=record.blockNumber, timeStamp=record.timeStamp,
                      value=record.value, name='', level=0)

    find_tracing(fatherNode, record)

    print(fatherNode.as_json())


if __name__ == '__main__':
    eth_address = '0x006922CF75094708c691d06818034d89aeB23ca0'
    tx_hash = '0xbc2b5ec6863fe320a8f72e25ec6ab277ed9d08e25913e6fa0c53866d30dd8d11'

    search_hash(eth_address, tx_hash)
    #
    # transactions = api.get_all_transactions(sort='desc', internal=False, start_block=5000000)
    #
    # for trans in transactions:
    #     count = Record.select().where(Record.hash == trans['hash']).count()
    #     if count <= 0:
    #         Record.insert(blockNumber=int(trans['blockNumber']),
    #                       timeStamp=int(trans['timeStamp']),
    #                       hash=trans['hash'], account=trans['from'], to=trans['to'],
    #                       value=int(trans['value']) / 10 ** 18).execute()
