# coding=utf-8
import time
from urllib import urlencode

import requests
import log

logging = log.getLogger('api.log')

# 百度地图api
class BdMap:
    # api ak
    api_ak = 'hRiVKsRGUykDoA2UAl5tNGpGYw15alaK'

    # 单次最大信息数
    page_size = 20

    # 单次最大出错次数
    error_max = 10

    # 构造函数 传入秘钥
    def __init__(self):
        self.raw_map = {
            'ak': self.api_ak,
            'output': 'json',
            'scope': '2',
            'page_size': self.page_size
        }
        return

    # 地域检索api
    def region_search(self, query, tag, region, get_all=True):
        url = Url('https://api.map.baidu.com/place/v2/search')
        url.set_map(self.raw_map)

        params = {
            'query': query,
            'tag': tag,
            'region': region,
        }
        url.set_map(params)

        if get_all:
            return self._get_list(url)
        else:
            return self._get_result(url)

    # 圆形区域检索api
    # 查找请求, 经纬度(逗号分隔), 查找半径(米)
    def circle_search(self, query, tag, location, radius):
        url = Url('https://api.map.baidu.com/place/v2/search')
        url.set_map(self.raw_map)

        params = {
            'query': query,
#            'tag': tag,
            'location': location,
            'radius': radius,
        }

        url.set_map(params)
        results = self._get_list(url)

        logging.info('共{0}个结果'.format(str(len(results))))
        return results

    # 获取坐标
    def get_location(self, address, city=None):
        url = Url('http://api.map.baidu.com/geocoder/v2/')
        url.set_map(self.raw_map)

        url.set_param('address', address)
        if city:
            url.set_param('city', city)

        return self._get_result(url)

    # 批量算路
    def path_search(self, way, org_location, dst_locations):
        url = Url('https://api.map.baidu.com/routematrix/v2/{0}'.format(way))
        url.set_map(self.raw_map)

        paths = []
        index = 0
        num = 30
        while True:
            time.sleep(0.5)
            dsts = []
            if index >= len(dst_locations):
                break
            else:
                start = index
                end = min(index + num, len(dst_locations))
                dsts = dst_locations[start:end].copy()
                index += num
            params = {'origins': org_location, 'destinations': '|'.join(dsts)}
            url.set_map(params)
            logging.info(url)
            paths += self._get_result(url)
        return paths

    # 获取请求信息
    def _get_result(self, url):
        error_flag = 0
        json = {}
        while True:
            time.sleep(0.5)
            if (error_flag > self.error_max):
                logging.error('错误次数超过{0}'.format(self.error_max))
                self.on_error(json)
                break
            try:
                r = requests.get(url)
                json = r.json()
                status = json['status']
                if status == 0:
                    # 请求成功
                    result = json['result']
                    return result
                else:
                    # 请求失败
                    error_flag += 1
                    logging.warning(json['message'])
                    continue
            except requests.exceptions.RequestException:
                logging.error('网络连接异常')
                return None
            except KeyError:
                logging.warning(json['msg'])

    # 获取请求列表
    def _get_list(self, url):
        page_num = 0
        error_flag = 0

        total_results = []
        json = {}
        while True:
            time.sleep(0.5)
            if (error_flag > self.error_max):
                logging.error('错误次数超过{0}'.format(self.error_max))
                self.on_error(json)
                break
            try:
                url.set_param('page_num', page_num)
                r = requests.get(url)
                json = r.json()
                status = json['status']
                if status == 0:
                    # 请求成功
                    results = json['results']
                    # print(results)
                    logging.info(url)
                    # print(len(results))
                    if len(results) == 0:
                        # 结束迭代
                        # print('结束')
                        break
                    else:
                        # 继续迭代
                        total_results += results
                        page_num += 1
                        continue
                else:
                    # 请求失败
                    error_flag += 1
                    logging.warning(str(json['message']) + str(url))
                    continue
            except requests.exceptions.RequestException:
                logging.error('网络连接异常')
                return None
        return total_results

    def on_error(self, json):
        # print('错误超过{0}次, 已暂停'.format(self.error_max))
        logging.error(json)
        raise
    pass

# Url管理
class Url:
    # 构造函数 传入唯一资源定位地址
    def __init__(self, p_url):
        self.url = p_url
        self.param_map = {}
        return

    # 传出Url字符串
    def __str__(self):
        query_param = urlencode(self.param_map)
        return self.url + '?' + query_param

    # 设置参数
    def set_param(self, key, value):
        self.param_map[key] = value
        return

    # 批量设置参数
    def set_map(self, map):
        self.param_map.update(map)
        return

    # 清空参数
    def clear_map(self):
        self.param_map = {}
        return

    pass

