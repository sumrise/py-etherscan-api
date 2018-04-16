#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/13 下午2:25
# @Author  : sumrise
# @Site    : 
# @File    : statMoney.py
# @Software: PyCharm
import json
import logging

from etherscan.accounts import Account

q = ["0xb9164cfcdf390d2ebf6d407857accc9ac7419e10", "0x7cfc7661c43842ce5f34feb23aee3c8afc3de4f5",
     "0x51bfe94b5db556a0665b4799f5fe6c8ee0aad52c", "0x4408a18b3d4aceb844a195695c62485653b07bb3",
     "0x2a82a908651099bd073ca6aea055e170066bf1b1", "0xdeabe2086ba80f77d40086656c51a200fe710273",
     "0xe70b1e81224212c3aef38917174f958abfda67f2", "0x495c11a1e2e65db95b59fa06dc274aaedce55981",
     "0x434e8b379f0ea5a5b88472b0792ec515dbc247c8", "0xa53946fd894719b6b6376c34d6f59439bcfe7475",
     "0x1b57b5e158c77c5e8470f8d8fb3aab08d4b0da6b", "0xdd14a3f9ed0c5a273944bd7bbb6d03c7560c8256",
     "0x24b862fdaa37db0bc171d91cc79c1f9ca1c9438e", "0x58c964e7994e06653efcdb9385a683e026be9853",
     "0x159ccb8cf4f4b4a6d242143ce7573b8e36fa908f", "0xa63ee20bd24b207cf83e332ee06077915130b3f9",
     "0xe06ed1d71c9fb622d4f89f993b90e4f55115f11f", "0x1641f424dd20b42e13eca92ad40bbc7a37838148",
     "0xb8bce40fd785cae38a4b1b8a4ea22466afdeadab", "0x6ae885c81147f242f79fb6586c59631c03b0f50f",
     "0x8a95ac9287e67eb6c42141e26be6d692598a6aff", "0xba3e607241b31d584ee80a2d34d5dd8014e57859",
     "0x1b7e9dd081536d3f9e041899980c9233cc5656dd", "0xacfa3cf23bdd26ba66332730704af88dcd6855fa",
     "0xe13024aaa06b4495fddda541d2be7111c3adc13c", "0x9cd65cb178dc90e5ed9b1845586af7c2139dbfc4",
     "0x455716d01f0280b2ce4282400ea07eee1231fdb5", "0xe68dd1aa5ce40efa50ce758e6d4c3425f391a887",
     "0x95f30481a7181651368c923a71190888d5a03607", "0x73d0291b07135e298494229098cc625f0c24676c",
     "0x6d4ba1ee6cea82499a05c3a6819de6e168c67d1a", "0xbe0a8274f660a6f94bcb2e2777c04360f36d25da",
     "0x83397e3f4ca443091153f78b547d063dc8d83d9b", "0xacfac287c811169a4e7fc0788aea8ff97d59fa0f",
     "0x9e91b1fb46e4408b2c57af64140623479c35dc87", "0x3ba50b16c3ea3ec360740063361776bfa133686d",
     "0x2c925bb3807545bd39b1040276c53c52f0d1298c"]

all_money = 0

with open('../../api_key.json', mode='r') as key_file:
    key = json.loads(key_file.read())['key']

eth_list = [i.strip() for i in open('eth_list', 'r')]
contract_dict = {
    'nv': '0x809826cceab68c387726af962713b64cb5cb3cca',
    'mytoken': '0x9b4e2b4b13d125238aa0480dd42b4f6fc71b37cc'
}
for address in eth_list:
    try:
        api = Account(address=str(address), api_key=key)  #
        balance = api.get_balance_token(contract_address=contract_dict['mytoken'])
        if int(balance) > 0:
            logging.info(balance)
            s = int(balance) / 10 ** 18
            all_money += s
            print(address + "              " + str(balance))
            # if s != 800:
            #     print(address)
    except Exception as e:
        print(e)

print(all_money)
