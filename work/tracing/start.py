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
def find_all_transactions(address, start_block, hash=''):
    if address in address_map:
        name = address_map[address]
        return name

    api = Account(address=address, api_key=key)
    transactions = api.get_all_transactions(sort='desc', start_block=start_block)
    if len(transactions) > 2000:
        address_map[address] = str(len(transactions)) + '某交易所'
        logging.info('xxxxxxxxxxxxxxxxx----------' + address + '---------xxxxxxxxxxxxx')
    for trans in transactions:
        count = Record.select().where(Record.hash == trans['hash']).count()
        if count <= 0:
            Record.insert(blockNumber=int(trans['blockNumber']),
                          timeStamp=int(trans['timeStamp']),
                          hash=trans['hash'], account=trans['from'], to=trans['to'],
                          value=int(trans['value']) / 10 ** 18).execute()

        if hash == trans['hash']:
            break
    records = Record.select().where(Record.account == address).order_by(Record.blockNumber)

    return records


# 追踪地址 开始hash,地址，开始区块
def find_tracing(nodeChain, record, dept=0, level=0):
    if dept >= 3:
        return
    logging.info('----------深度' + str(dept) + '----------')
    logging.info(nodeChain.as_json())
    if nodeChain.address in address_map:
        nodeChain.name = address_map[nodeChain.address]
        return
    else:
        childNode = newNode(nodeChain, record, level)

        next_transactions = find_all_transactions(childNode.address, childNode.blockNumber)  #
        if type(next_transactions) is str:
            childNode.name = next_transactions
            return
        results222 = [ob.as_json() for ob in next_transactions]
        results222 = json.dumps(results222)
        print(childNode.address)
        logging.info("转账记录：" + results222)
        if len(next_transactions) <= 0:
            logging.info("next_transactions:" + next_transactions)
            return
        logging.info('----start----' + next_transactions[0].hash)

        isfind = False
        hashList = [a.hash for a in next_transactions]
        blcokerList = [a.blockNumber for a in next_transactions]

        # api = Account(address=childNode.address, api_key=key)
        # balance = api.get_balance_token(contract_address='0x809826cceab68c387726af962713b64cb5cb3cca')
        # if int(balance) > 0:
        #     logging.info(balance)

        width = 1
        x = record.hash in hashList
        for to_node in next_transactions:  # 跳过
            # if to_node.hash == record.hash:
            #     isfind = True
            if childNode.value == 0 or to_node.value == 0 or width > 3:
                continue

            if to_node.account == childNode.address:  # 发出
                logging.info(str(to_node.value) + "---" + str(childNode.value))
                if to_node.value == childNode.value:
                    # into
                    find_tracing(childNode, to_node, dept + 1, 0)
                    width += 1
                elif to_node.value - childNode.value > 0.1:
                    find_tracing(childNode, to_node, dept + 1, level + 1)
                    width += 1
                elif abs(to_node.value - childNode.value) <= 5:
                    find_tracing(childNode, to_node, dept + 1, level + 1)
                    width += 1
                else:
                    pass

    logging.info('------深度' + str(dept) + ' ----end  ----------')


def newNode(fatherNode, record, level=0):
    childNode = Node(hash=record.hash, address=record.to, blockNumber=record.blockNumber,
                     timeStamp=record.timeStamp,
                     value=record.value, level=level, name='')
    fatherNode.children.append(childNode)

    return childNode


def search_hash(address, hash):
    records = find_all_transactions(address, 0, hash)
    record = records[0]

    fatherNode = Node(hash=hash, address=address, blockNumber=0, timeStamp=0,
                      value=0, name='', level=0)

    find_tracing(fatherNode, record)

    logging.info('result = ')
    print(fatherNode.as_json())


if __name__ == '__main__':
    eth_address = '0xa5836a97da9f714238d4481d6bccb87789d84fdc'
    tx_hash = '0xe114db3ec35b0961880fe460cb80675a6835ced690a930547833329d931f11ec'

    # 两种模式 一种清库，一种不清
    clear_db = True
    if clear_db:
        Record.delete().where(Record.id > 0).execute()

    search_hash(eth_address, tx_hash)
