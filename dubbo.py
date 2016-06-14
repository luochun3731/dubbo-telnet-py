#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import telnetlib


class dubbo:
    # 定义私有属性,私有属性在类外部无法直接进行访问
    __init = False
    __encoding = "gbk"
    __finish = 'dubbo>'
    __connect_timeout = 10

    # 定义构造方法
    def __init__(self, host, port):
        self.host = host
        self.port = port
        if host is not None and port is not None:
            self.__init = True

    def set_finish(self, finish):
        self.__finish = finish

    def set_encoding(self, encoding):
        self.__encoding = encoding

    def set_connect_timeout(self, timeout):
        self.__connect_timeout = timeout

    def do(self, command):
        # 连接Telnet服务器
        tn = telnetlib.Telnet(host=self.host, port=self.port, timeout=self.__connect_timeout)

        # 触发doubble提示符
        tn.write('\n')

        # 执行命令
        tn.read_until(self.__finish)
        tn.write('%s\n' % command)

        # 获取结果
        data = ''
        while data.find(self.__finish) == -1:
            data = tn.read_very_eager()
        data = data.split("\n")
        data = json.loads(data[0], encoding="gbk")

        tn.close()  # tn.write('exit\n')

        return data

    def invoke(self, interface, method, param):
        cmd = "%s %s.%s(%s)" % ('invoke', interface, method, param)
        return self.do(cmd)


if __name__ == '__main__':
    Host = '192.168.1.203'  # Doubble服务器IP
    Port = 28008  # Doubble服务端口

    # 初始化dubbo对象
    conn = dubbo(Host, Port)

    # 设置telnet连接超时时间
    conn.set_connect_timeout(10)

    # 设置dubbo服务返回响应的编码
    conn.set_encoding('gbk')

    interface = 'com.zrj.pay.trade.api.QueryTradeService'
    method = 'tradeDetailQuery'
    param = '{"id": "nimeide"}'
    print conn.invoke(interface, method, param)

    command = 'invoke com.zrj.pay.trade.api.QueryTradeService.tradeDetailQuery({"id":"nimeide"})'
    print conn.do(command)
