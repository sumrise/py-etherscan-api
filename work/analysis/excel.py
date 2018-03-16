#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/6 下午6:12
# @Author  : sumrise
# @Site    : 
# @File    : excel.py
# @Software: PyCharm


import os
import xlwt


class XlsReport:
    #    '''Excel报告接口'''
    def __init__(self, file_path):
        self.xls_workbook = None  # 创建的Excel对象
        self.xls_file_path = file_path  # 创建Excel的文件路径
        self.xls_worksheets = {}  # 工作表的行列标记符{worksheet对象:{r:行,c:列}}
        self.xls_sheet_col_length = {}  # 工作表的列宽{worksheet对象:{列1:宽度,列2:宽度...}}

    def xlsOpenWorkbook(self):
        '''创建一个Excel'''
        self.xls_workbook = xlwt.Workbook(style_compression=2)

    def xlsAddWorksheet(self, sheet_name='sheet', r=0, c=0):
        '''
        创建一个工作表对象
        @parameter sheet_name:工作簿名称
        @parameter r:工作表的行
        @parameter c:工作表的列
        '''
        obj_worksheet = self.xls_workbook.add_sheet(sheet_name)  # 创建工作表对象
        xls_worksheet = {}  # 工作表的行列标记符
        xls_worksheet['r'] = r  # 行标记符
        xls_worksheet['c'] = c  # 列标记符
        self.xls_worksheets[obj_worksheet] = xls_worksheet
        self.xls_sheet_col_length[obj_worksheet] = {}
        return obj_worksheet

    def xlsCloseWorkbook(self, obj_worksheet):
        '''
        关闭Excel文件对象,保存Excel数据
        @parameter obj_worksheet:工作表对象
        '''
        # 设置工作簿的列宽
        for c in self.xls_sheet_col_length[obj_worksheet]:
            if self.xls_sheet_col_length[obj_worksheet][c] < 10:
                obj_worksheet.col(c).width = 256 * 10
            elif self.xls_sheet_col_length[obj_worksheet][c] > 50:
                obj_worksheet.col(c).width = 256 * 50
            else:
                obj_worksheet.col(c).width = 256 * (self.xls_sheet_col_length[obj_worksheet][c])
        # 关闭工作表对象
        self.xls_workbook.save(self.xls_file_path)

    def addWorksheetTitle(self, obj_worksheet, titles=[], r=0, c=0):
        '''
        添加工作簿的标题
        @parameter obj_worksheet:工作表对象
        @parameter titles:标题
        @parameter r:工作表的行
        @parameter c:工作表的列
        '''
        # 设置标题的样式
        style_title = xlwt.easyxf('pattern:pattern solid,fore_colour lime; font:height 200,bold on; align:horz center;')
        # 写工作簿的标题
        for title in titles:
            obj_worksheet.write(r, c, title, style_title)
            c += 1
        # 工作簿的行标记+1
        r += 1
        self.xls_worksheets[obj_worksheet]['r'] = r

    def appendWorkshetData(self, obj_worksheet, datas=[], r=None, c=None, gold=0):
        '''
        按行追加数据
        @parameter obj_worksheet:工作表对象
        @parameter datas:标题
        @parameter r:工作表的行
        @parameter c:工作表的列
        @parameter gold:0(不变/Pass),-1(变差/Fail),1(变好)
        '''
        # 标准
        stylebox = xlwt.easyxf('font:height 200; borders:left 1,right 1,top 1,bottom 1; align:horiz left,wrap 1')
        # 红体
        stylebox_red = xlwt.easyxf(
            'font:height 200,color-index red; borders:left 1,right 1,top 1,bottom 1; align:horiz left,wrap 1')
        # 蓝体
        stylebox_blue = xlwt.easyxf(
            'font:height 200,color-index blue; borders:left 1,right 1,top 1,bottom 1; align:horiz left,wrap 1')
        # 写工作表的行
        if None == r:
            r = self.xls_worksheets[obj_worksheet]['r']
        else:
            r = r
        # 写工作表的列
        if None == c:
            c = self.xls_worksheets[obj_worksheet]['c']
        else:
            c = c
        # 写工作表的数据
        for data in datas:
            if str != type(data):
                data = str(data)
            if 0 == gold:
                obj_worksheet.write(r, c, data, stylebox)
            elif -1 == gold:
                obj_worksheet.write(r, c, data, stylebox_red)
            elif 1 == gold:
                obj_worksheet.write(r, c, data, stylebox_blue)
            else:
                print('Info:gold was illegal.')
                obj_worksheet.write(r, c, data, stylebox)
            # 工作表每列的最大字符长度
            if c not in self.xls_sheet_col_length[obj_worksheet]:
                self.xls_sheet_col_length[obj_worksheet][c] = len(data)
            else:
                if self.xls_sheet_col_length[obj_worksheet][c] < len(data):
                    self.xls_sheet_col_length[obj_worksheet][c] = len(data)
            c += 1
        # 工作表的行标记+1
        r += 1
        self.xls_worksheets[obj_worksheet]['r'] = r


# self test
if __name__ == '__main__':
    # 文件的后缀名为xls
    file_path = os.path.join(os.getcwd(), 'test.xls')
    xls = XlsReport(file_path)
    # 创建Excel对象
    xls.xlsOpenWorkbook()
    # xls.addWorksheetTitle('Credits')
    # 添加工作对象
    sheet_names = ['sheet1', 'sheet2', 'sheet3']
    for sheet_name in sheet_names:
        sheet = xls.xlsAddWorksheet(sheet_name)
        # Excel的标题
        xls.addWorksheetTitle(sheet, ['时间', 'From', 'To', '数量'])
        # Excel的数据
        xls.appendWorkshetData(sheet, [1001, 'test1', 'Pass', ''])
        xls.appendWorkshetData(sheet, [1002, 'test2', 'Fail', '失败'])
        xls.appendWorkshetData(sheet, [1003, 'test3', 'Pass', '调优'])
        xls.xlsCloseWorkbook(sheet)
