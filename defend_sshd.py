#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, re
import time
import platform


class DefendSSH():

    def __init__(self, sys, black, trust):

        self.sys_issue = sys
        self.backList = black
        self.trust_ip = trust
        self.base_dir = '/var/log'
        self.auth_log = os.path.join(self.base_dir, 'auth.log')

        if self.sys_issue == 'centos':
            self.auth_log = os.path.join(self.base_dir, 'secure')


    def parser_log(self, log):
        """
        解析日志文件,返回正则表达式匹配的列表.
        :param log: 日志文件路径
        :return: list
        """

        string = ''
        month = time.asctime().split()[1]
        day = time.asctime().split()[2]

        with open(log, 'r') as F:
            string = F.read()
            F.close()

        result = re.findall(r'%s %s .*: (.* \d+\.\d+\.\d+\.\d+)' % (month, day), string)

        return result


    def unique_id(self, item):
        """
        使用set() 去掉重复的元素
        :param item: 列表
        :return: list
        """

        result = set()

        for i in item:
            result.add(i.split()[-1])

        return list(result)


    def cmp(self):
        # value = ['Disconnected from 114.32.120.181', 'Invalid user chris from 114.32.120.181', ..]
        # key = ['114.32.120.181', ..]
        # result = {key: list.count(k)}

        result = {}
        new_values = []

        values = self.parser_log(self.auth_log)
        keys = self.unique_id(values)

        for v in values:

            # trust_ip or 'Accepted' keyWord
            if v.split()[0] == 'Accepted' or v.split()[-1] in self.trust_ip:
                if v.split()[-1] in keys:
                    keys.remove(v.split()[-1])

            new_values.append(v.split()[-1])

        for k in keys:
            result[k] = new_values.count(k)

        return result


    def add_blacklist(self,item ,num=5):
        """
        将IP 添加到黑名单文件 "/etc/hosts.deny"
        :param item: 字典
        :param num: 默认条件
        :return: Na
        """

        with open(self.backList, 'w+') as F:

            # 按照 value/次数 倒序排序。
            for k, v in sorted(item.items(), key=lambda h: h[1], reverse=True):

                if v >= num:
                    F.write("sshd:%s \n" % k)

            F.close()


if __name__ == '__main__':

    system = platform.dist()[0]
    black_list = '/etc/hosts.deny'
    trust_list = ['8.8.8.8']
    now = time.strftime("%Y-%m-%d %H:%M:%S")

    df = DefendSSH(system, black_list, trust_list)
    res = df.cmp()
    print(now,res)

    if res:
        df.add_blacklist(res,10)

