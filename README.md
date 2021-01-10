# IP_Proxies
代理IP池

需要先启动Redis数据库

打开run_pool.py更改你的数据库地址

把上面的参数改成你所需要的，爬取ip的数量，池中的IP的数量，http、https或者两者都需要，池刷新频率

http代理ip在redis中的键名为http，https则是https（存为列表，非集合）

随便用flask在网页上展示了池中的IP。
