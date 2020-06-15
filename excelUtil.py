# coding=utf-8
import xlwt
import time


class ExeclUtil:

    def __init__(self):
        pass

    def generate_doc(self, content):
        book = xlwt.Workbook(encoding='utf-8')
        sheet = book.add_sheet('baidu')
        title = ['名称', '地址', '电话', '详情网址']

        # 写入表头
        i = 0
        for j in title:
            sheet.write(0, i, j)
            i += 1

        # 写入表内容
        l = 1
        for cc in content:
            sheet.write(l, 0, cc['name'])
            sheet.write(l, 1, cc['address'])
            if cc.has_key('telephone'):
                sheet.write(l, 2, cc['telephone'])
            l += 1
            sheet.write(l, 3, cc['detail_info']['detail_url'])

        # 列宽度
        sheet.col(0).width = 10000
        sheet.col(1).width = 20000
        sheet.col(2).width = 5000


        # 保存
        book.save('/Users/maojing/Desktop/baidu_map/baidu//bd_%s.xls' % time.strftime("%m%d%H%M", time.localtime()))
