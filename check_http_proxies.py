
from aiohttp import ClientSession,ClientTimeout
import asyncio
import redis


http_quantity = 0

def action(conn,CHECK=False):
    global http_quantity
    async def check_http_proxy(ip):
        url = "http://www.baidu.com"
        async with ClientSession() as session:
            try:
                timeout = ClientTimeout(total=5)
                async with await session.get(url,proxy=ip,timeout=timeout) as response:
                    if response.status == 200:
                        print(ip+" 是可用HTTP 代理IP！!")
                        conn.rpush('http',ip)
            except Exception:
                print('丢弃不可用IP代理=>'+ ip)	

    http_ip_list = []
    if CHECK == False:
        for i in range(conn.llen('http')-http_quantity):
            ip = conn.lpop('http').decode('utf-8')
            http_ip_list.append(ip)
    else:
        for i in range(conn.llen('http')):
            ip = conn.lpop('http').decode('utf-8')
            http_ip_list.append(ip)

    
    tasks = []

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    for ip in http_ip_list:
        coroutine = check_http_proxy(ip)
        task = asyncio.ensure_future(coroutine, loop=loop)
        tasks.append(task)
        
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

    http_quantity = conn.llen('http')
    
if __name__ == "__main__":
    action(conn)

    