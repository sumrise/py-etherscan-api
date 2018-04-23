#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : findAddress.py
# @Author: sum
# @Date  : 2018/4/22
# @Desc  :


eth_list = [i.strip() for i in open('eth_address','r')]

wallet_list = [i.strip() for i in open('private','r')]


for wallet in wallet_list:
    address = wallet.split('\t')
    if address[0] in eth_list:
        print(address[1])
