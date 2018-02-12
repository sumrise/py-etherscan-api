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

logger = logging.getLogger('peewee')
logger.setLevel(logging.INFO)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

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
    if address in address_map:
        name = address_map[address]
        return name
    records = Record.select().where(Record.account == address)
    if len(records) <= 0:
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
def find_tracing(fatherNode, record, dept=0, level=0):
    logging.info('----------深度' + str(dept) + '----------')
    logging.info(fatherNode.as_json())
    if fatherNode.address in address_map:
        fatherNode.name = address_map[fatherNode.address]
        return
    else:
        childNode = newNode(fatherNode, record, level)
        next_transactions = find_all_transactions(childNode.address, record.blockNumber)
        if (type(next_transactions) is str):
            childNode.name = next_transactions
            return
        results222 = [ob.as_json() for ob in next_transactions]
        results222 = json.dumps(results222)
        logging.info('转账记录：' + results222)
        if len(next_transactions) <= 0:
            pass
        logging.info('----start----' + next_transactions[0].hash)

        isfind = False

        hashList = [a.hash for a in next_transactions]
        x = record.hash in hashList
        for to_node in next_transactions:  # 跳过
            # if to_node.hash == record.hash:
            #     isfind = True
            if to_node.account == childNode.address:  # 发出
                logging.info(str(to_node.value) + "---" + str(childNode.value))
                if to_node.value == childNode.value:
                    find_tracing(childNode, to_node, dept + 1, 0)
                if to_node.value - childNode.value > 0.01:
                    find_tracing(childNode, to_node, dept + 1, level + 1)

    logging.info('----------end  ----------')


def newNode(fatherNode, record, level=0):
    childNode = Node(hash=record.hash, address=record.to, blockNumber=record.blockNumber,
                     timeStamp=record.timeStamp,
                     value=record.value, level=level, name='')
    fatherNode.children.append(childNode)

    return childNode


def search_hash(address, hash):
    records = Record.select().where(Record.hash == hash)
    if len(records) > 0:
        logging.info(records[0])
    else:
        records = find_all_transactions(address, 0)

    record = records[0]
    fatherNode = Node(hash='', address=address, blockNumber=0, timeStamp=0,
                      value=0, name='', level=0)

    # nextNode = Node(hash=record.hash, address=record.to, blockNumber=record.blockNumber, timeStamp=record.timeStamp,
    #                 value=record.value, name='', level=0)
    #
    # nextNode =
    find_tracing(fatherNode, record)

    logging.info('result = ')
    print(fatherNode.as_json())


if __name__ == '__main__':
    eth_address = '0x006922CF75094708c691d06818034d89aeB23ca0'
    tx_hash = '0xbc2b5ec6863fe320a8f72e25ec6ab277ed9d08e25913e6fa0c53866d30dd8d11'

    # 两种模式 一种清库，一种不清
    clear_db = True
    if clear_db:
        Record.delete().where(Record.id > 0).execute()

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
