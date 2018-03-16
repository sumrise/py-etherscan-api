#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/6 下午4:47
# @Author  : sumrise
# @Site    : 
# @File    : big_dog.py
# @Software: PyCharm

# 分析狗庄
import os
import requests
from bs4 import BeautifulSoup

import xlwt

from analysis.excel import XlsReport
from analysis.model import Transaction

url = 'https://etherscan.io/token/generic-tokentxns2'
headers = {
    'cookie': '__cfduid=db80c0c3b258d47889635bb51145ca35a1511784192; _ga=GA1.2.1596100347.1511784194; etherscan_userid=fu189; etherscan_pwd=4792:Qdxb:avbdJbrX4drZX2AlIx8uDQ==; etherscan_autologin=True; ASP.NET_SessionId=udog2rgc4lpjwibb3z50hc5d; __cflb=4117770365; _gid=GA1.2.1656355725.1520312532; cf_clearance=ff1a5bd9da73b2f80f7a5addade0c7ac9381887e-1520391703-2700; _gat_gtag_UA_46998878_6=1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'authority': 'etherscan.io',
    'referer': 'https://etherscan.io/token/generic-tokentxns2?contractAddress=0x46b9ad944d1059450da1163511069c718f699d31&mode=&p=6',
}


def download_html(address, page=139):
    params = (
        ('contractAddress', '0x46b9ad944d1059450da1163511069c718f699d31'),
        ('a', address),
        ('mode', ''),
        ('p', str(page)),
    )
    response = requests.get('https://etherscan.io/token/generic-tokentxns2', headers=headers, params=params)

    soup = BeautifulSoup(response.content, "html.parser")

    trans = soup.select('table.table tr')
    trans = trans[1:]
    if (len(trans) != 50):
        print(str(page) + '   ' + str(len(trans)))

    transList = toModels(trans)

    # results = [ob.as_json() for ob in transList]

    return transList


def toModels(trans):
    returnList = []
    for i in range(len(trans)):
        td = trans[i].select('td')
        date = td[1].span['title']
        account = td[2].span.text
        to = td[4].span.text
        value = td[5].text.replace(',', '')

        a = Transaction(account, to, value, date)

        returnList.append(a)

    return returnList


def toExcel():
    file_path = os.path.join(os.getcwd(), 'credits156.xls')
    xls = XlsReport(file_path)
    # 创建Excel对象
    xls.xlsOpenWorkbook()
    # xls.addWorksheetTitle('Credits')
    # 添加工作对象

    num = [183, 59, 15]
    address = ['0x2a0c0dbecc7e4d658f48e01e3fa353f44050c208',
               '0x0a73573cf2903d2d8305b1ecb9e9730186a312ae',
               '0x2b5634c42055806a59e9107ed44d43c426e58258']

    sheet_names = ['sheet1', 'sheet2', 'sheet3']
    for sheet_name in sheet_names:
        sheet = xls.xlsAddWorksheet(sheet_name)
        # Excel的标题
        xls.addWorksheetTitle(sheet, ['时间', 'From', 'To', '数量'])
        # Excel的数据

        for i in range(num[sheet_names.index(sheet_name)], -1, -1):
            transList = download_html(address[sheet_names.index(sheet_name)], page=i)
            for trans in transList:
                try:
                    xls.appendWorkshetData(sheet, [trans.date, trans.account, trans.to, float(trans.value)])
                except Exception as e:
                    print(e)
                    print(trans)
        xls.xlsCloseWorkbook(sheet)


if __name__ == '__main__':
    sumList = []
    # for i in range(152, -1, -1):
    #     transList = download_html(i)
    #     sumList.append(transList)
    # sumList = download_html(152)

    toExcel()
