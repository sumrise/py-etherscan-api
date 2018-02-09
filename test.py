#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/2 上午11:19
# @Author  : sumrise
# @Site    : 
# @File    : test.py
# @Software: PyCharm

# 1985年09月27日
import requests

url = 'https://15tianqi.cn/sfz/'

form_date = {
    'idcardno': '610202199210212414',
    'uname': '',
    'submit': '开始查询'
}


def xx():
    content = requests.post(url=url, data=form_date).content
    content = str(content, 'utf-8')
    if content.find(u'18位完整号码') > 0:
        print('xxx')
    print(content)


def caculate_last(idcardno):
    Wi = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    IndexTable = {  # 此处实际是无需使用字典的，使用一个包含11个元素的数组便可，数组中存放
        0: '1',  # 相应位置的号码，但是这也正好演示了Python高级数据结构的使用
        1: '0',
        2: 'x',
        3: '9',
        4: '8',
        5: '7',
        6: '6',
        7: '5',
        8: '4',
        9: '3',
        10: '2'
    }
    No = []
    sum = 0
    if len(idcardno) != 17:
        print("error number")
    for x in idcardno:
        No.append(int(x))
    for i in range(17):
        sum = sum + (int(No[i]) * Wi[i])
    Index = sum % 11
    return idcardno + str(IndexTable[Index])


if __name__ == '__main__':
    idc = '44011119850927000'

    No = [i for i in idc]

    XX=[]

    for i in range(10):
        No[-3] = str(i)
        for j in range(10):
            No[-2] = str(j)
            for k in range(10):
                No[-1] = str(k)
                idcard = caculate_last(''.join(No))
                # print("'" + idcard + "'" + ',')
                XX.append( idcard )

    print (XX)