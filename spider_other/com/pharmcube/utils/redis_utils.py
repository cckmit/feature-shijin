#!/usr/bin/env python
# coding:utf-8

'''
python3 使用redis集群
'''

from rediscluster import StrictRedisCluster

def redis_cluster(debug):
    redis_nodes = []
    if 'true' == debug: #本地环境
        redis_nodes = [{'host': '192.168.1.136', 'port': 8000},
                       {'host': '192.168.1.136', 'port': 8001},
                       {'host': '192.168.1.136', 'port': 8002},
                       {'host': '192.168.1.136', 'port': 8003},
                       {'host': '192.168.1.136', 'port': 8004},
                       {'host': '192.168.1.136', 'port': 8005},]
    elif 'test' == debug:#测试环境
        redis_nodes = [{'host': '172.24.56.160', 'port': 8000},
                       {'host': '172.24.56.160', 'port': 8001},
                       {'host': '172.24.56.160', 'port': 8002},
                       {'host': '172.24.56.160', 'port': 8003},
                       {'host': '172.24.56.160', 'port': 8004},
                      {'host': '172.24.56.160', 'port': 8005},]
    else: #线上环境
        redis_nodes = [{"host": "10.66.205.48", "port": 8000},
                                                  {"host": "10.66.205.48", "port": 8001},
                                                  {"host": "10.66.205.48", "port": 8002},
                                                  {"host": "10.66.205.48", "port": 8003},
                                                  {"host": "10.66.205.48", "port": 8004},
                                                  {"host": "10.66.205.48", "port": 8005},
                                                  {"host": "10.66.205.48", "port": 8006},
                                                  {"host": "172.17.108.71", "port": 8000},
                                                  {"host": "172.17.108.71", "port": 8001},
                                                  {"host": "172.17.108.71", "port": 8002},
                                                  {"host": "172.17.108.71", "port": 8003},
                                                  {"host": "172.17.108.71", "port": 8004},
                                                  {"host": "172.17.108.71", "port": 8005},
                                                  {"host": "172.17.108.71", "port": 8006},
                                                  {"host": "172.17.108.71", "port": 8007}]
    return StrictRedisCluster(startup_nodes=redis_nodes, decode_responses=True, max_connections=15, skip_full_coverage_check=True)
