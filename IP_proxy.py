import redis
import requests
from lxml import etree
from multiprocessing.dummy import Pool
from multiprocessing import Lock
from aiohttp import ClientSession
import asyncio

class Proxy:
    #conn = redis.Redis(host='127.0.0.1', port=6379)
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47"}
    http_page_num = 1
    https_page_num = 1
    https_QTY = 0
    lock = Lock()

    def __init__(self, conn):
        self.conn = conn


    def get_http_proxy(self,num): 
        http_proxy_url = f"http://www.nimadaili.com/http/{Proxy.http_page_num}/"
        while self.conn.llen('http') < num:
            resp = requests.get(url=http_proxy_url, headers=self.headers).text
            tree = etree.HTML(resp)
            http_ip_list = tree.xpath('/html/body/div/div[1]/div/table//tr/td[1]/text()')
            http_ip_list = [self.conn.lpush('http','http://'+ip) for ip in http_ip_list]
            Proxy.http_page_num += 1
            print('Redis数据库有HTTP代理IP数量为：',self.conn.llen('http'))

    def get_https_proxy(self,num): 
        https_proxy_url = f"http://www.nimadaili.com/https/{Proxy.https_page_num}/"
        while self.conn.llen('https') < num:
            resp = requests.get(url=https_proxy_url, headers=self.headers).text
            tree = etree.HTML(resp)
            https_ip_list = tree.xpath('/html/body/div/div[1]/div/table//tr/td[1]/text()')
            https_ip_list = [self.conn.lpush('https',ip) for ip in https_ip_list]
            Proxy.http_page_num += 1
            print('Redis数据库有HTTPS代理IP数量为：',self.conn.llen('https'))

    def check_https_proxy(self,ip):
        test_url = 'https://www.baidu.com'
        proxies={'https':ip}
        try:
            resp = requests.get(url=test_url,proxies=proxies, verify=False, headers=self.headers, timeout=5)
            if resp.status_code == 200:
                print(ip+" 是可用HTTPS 代理IP！")
                Proxy.lock.acquire()
                self.conn.rpush('https',ip)
                Proxy.lock.release()
        except Exception:
            print('丢弃不可用IP代理=>'+ ip)

    def multiprocessing_check_https_proxy(self):
        https_ip_list = []
        for n in range(self.conn.llen('https') - Proxy.https_QTY):
            ip = (self.conn.lpop('https')).decode('utf-8')
            https_ip_list.append(ip)
        pool = Pool()
        pool.map(self.check_https_proxy,https_ip_list)
        pool.close()
        pool.join()
        Proxy.https_QTY = self.conn.llen('https')


