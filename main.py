# coding=utf-8
import json

import log
from bdApi import BdMap
from excelUtil import ExeclUtil
logging = log.getLogger('api.log')


if __name__ == "__main__":


    print '******* 项目启动 ********'

    query = raw_input(unicode('搜索关键字：', 'gbk').encode('gbk'))
    location = raw_input(unicode('搜索坐标逗号分割: ', 'gbk').encode('gbk'))
    radius = raw_input(unicode('搜索范围: ', 'gbk').encode('gbk'))
    tag = ''
    #tag = '教育培训'
    #tag = '房地产'

    baiduApi = BdMap()
    rest = baiduApi.circle_search(query, tag, location, radius)
    logging.info(json.dumps(rest).decode())

    execlUtil = ExeclUtil()
    execlUtil.generate_doc(rest)

    print '采集完成，请到 "baidu" 目录下查找'
