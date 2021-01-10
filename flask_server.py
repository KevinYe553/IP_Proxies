from flask import Flask
import time
import random
import redis

conn = redis.Redis(host='127.0.0.1', port=6379)

app = Flask(__name__)

@app.route('/')
def proxies():
    return '代理IP池服务'

@app.route('/http')
def index_http_proxies():
    return random.choice(conn.lrange('http',1,-1))

@app.route('/https')
def index_https_proxies():
    return random.choice(conn.lrange('https',1,-1))


if __name__ == '__main__':
    app.run(threaded=True)