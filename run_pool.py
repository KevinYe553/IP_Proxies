from IP_proxy import Proxy
from check_http_proxies import action
import redis
import time

conn = redis.Redis(host='127.0.0.1', port=6379)
CRAWL_PROXIES_QTY = 100          #每次爬取的ip数（一般为50的倍数），假如100个ip里没有达到我们需要的可用数，将自动继续爬取，直到达到可用数为止。
AVAILABLE_PROXIES_QTY = 20       #可用代理数
WAITIME_TIME = 300              #刷新代理池的时间间隔（秒）
HTTP_OR_HTTPS = 'BOTH'

proxy = Proxy(conn)


def main(conn, CRAWL_PROXIES_QTY, AVAILABLE_PROXIES_QTY, WAITIME_TIME, HTTP_OR_HTTPS):
    print(f'启动线程池，当前线程池刷新频率为 {WAITIME_TIME} ,需要至少有 {AVAILABLE_PROXIES_QTY} 的可用代理IP数量！')
    while True:
        if HTTP_OR_HTTPS == 'HTTP' or HTTP_OR_HTTPS == 'BOTH':
            print('当前数据库中http代理IP数量为：',conn.llen('http'))
            if conn.llen('http') < AVAILABLE_PROXIES_QTY:
                proxy.get_http_proxy(CRAWL_PROXIES_QTY)
                action(conn)
            else:
                action(conn,CHECK=True)

       

        if HTTP_OR_HTTPS == 'HTTPS' or HTTP_OR_HTTPS == 'BOTH':
            print('当前数据库中https代理IP数量为：',conn.llen('https'))
            while conn.llen('https') < AVAILABLE_PROXIES_QTY:
                proxy.get_https_proxy(CRAWL_PROXIES_QTY)
                proxy.multiprocessing_check_https_proxy()   

        time.sleep(WAITIME_TIME)

        

if __name__ == "__main__":
    main(conn, CRAWL_PROXIES_QTY, AVAILABLE_PROXIES_QTY, WAITIME_TIME, HTTP_OR_HTTPS)
