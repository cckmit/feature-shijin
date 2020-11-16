#!/usr/bin/env python
# coding:utf-8

'''
python3 使用redis集群
'''

from rediscluster import StrictRedisCluster

def redis_cluster(debug):
    redis_nodes = []
    if 'true' == debug: #本地环境
        redis_nodes = [{'host': '192.168.1.136', 'port': 7000},
                       {'host': '192.168.1.136', 'port': 7001},
                       {'host': '192.168.1.136', 'port': 7002},
                       {'host': '192.168.1.136', 'port': 7003},
                       {'host': '192.168.1.136', 'port': 7004},
                       {'host': '192.168.1.136', 'port': 7005},]
    elif 'test' == debug:#测试环境
        redis_nodes = [{'host': '172.24.56.160', 'port': 7000},
                       {'host': '172.24.56.160', 'port': 7001},
                       {'host': '172.24.56.160', 'port': 7002},
                       {'host': '172.24.56.160', 'port': 7003},
                       {'host': '172.24.56.160', 'port': 7004},
                      {'host': '172.24.56.160', 'port': 7005},]
    else: #线上环境
        redis_nodes = [{'host': '10.46.176.105', 'port': 7000},
                       {'host': '10.46.176.105', 'port': 7001},
                       {'host': '10.46.176.105', 'port': 7002},
                       {'host': '10.46.176.105', 'port': 7003},
                       {'host': '10.46.176.105', 'port': 7004},
                       {'host': '10.46.176.105', 'port': 7005},
                       {'host': '10.27.217.54', 'port': 7000},
                       {'host': '10.27.217.54', 'port': 7001},
                       {'host': '10.27.217.54', 'port': 7002},
                       {'host': '10.27.217.54', 'port': 7003},
                       {'host': '10.27.217.54', 'port': 7004},
                       {'host': '10.27.217.54', 'port': 7005},
                       {'host': '10.27.217.22', 'port': 7000},
                       {'host': '10.27.217.22', 'port': 7001},
                       {'host': '10.27.217.22', 'port': 7002},
                       {'host': '10.27.217.22', 'port': 7003},
                       {'host': '10.27.217.22', 'port': 7004},]
    return StrictRedisCluster(startup_nodes=redis_nodes, decode_responses=True, max_connections=15, skip_full_coverage_check=True)
