#coding:utf8
from pyExcelerator import *

#处理对象为列表。该列表中包含列表，最终的列表包含的是两个元素的元组


class ExcelHandle:

    def __init__(self,list,filename):
        self.list = list
        self.filename = filename

    def Excel_Write(self):
        w = Workbook()          #创建一个工作簿
        ws = w.add_sheet("test1")  #创建一个工作表
        m = 0  # 行数
        n = 0  # 列数
        for i in range(len(self.list)):
            for j in self.list[i]:
                #print m,n
                ws.write(m,n,j[0])
                n = n + 1
                ws.write(m,n,j[1])
                n = n - 1
                m = m + 1
            n = n + 2
            m = 0
        w.save(self.filename + '.xls')

#库的使用格式
if __name__ == '__main__':
    list = [[(u"小王",123),(u"小张",456)],
            [(u"小李",789),(u"小吴",101)],
            [(u"小强",112),(u"阿凯",131)]]
    filename = 'haha'
    Excelhandle = ExcelHandle(list,filename)
    Excelhandle.Excel_Write()
