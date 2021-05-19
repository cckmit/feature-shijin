
# dev; test; prod; hk_prod
run_evn = 'dev'

def get_run_env_dict():
    run_evn_dict = {}
    if 'dev' == run_evn:
        run_evn_dict = {'mongo': {'host': '127.0.0.1', 'port': 27017, 'db': 'spider_py'}, 'es_addr': {"es_host": ("123.56.187.45",)}, 'redis':{'redis_nodes':[{"host":"192.168.1.136","port":"8000"},{"host":"192.168.1.136","port":"8001"},{"host":"192.168.1.136","port":"8002"},{"host":"192.168.1.136","port":"8003"},{"host":"192.168.1.136","port":"8004"},{"host":"192.168.1.136","port":"8005"},]}}
    elif 'test' == run_evn:
        run_evn_dict = {'mongo': {'host': '127.0.0.1', 'port': 27017, 'db': 'spider_py'}, 'es_addr': {"es_host": ("123.56.187.45",)}, 'redis':{'redis_nodes':[{"host": "172.24.56.160", "port": "8000"},{"host": "172.24.56.160", "port": "8001"},{"host": "172.24.56.160", "port": "8002"},{"host": "172.24.56.160", "port": "8003"},{"host": "172.24.56.160", "port": "8004"},{"host": "172.24.56.160", "port": "8005"},]}}
    elif 'hk_prod' == run_evn:
        run_evn_dict = run_evn_dict = {'mongo': {'host': '172.26.88.232', 'port': 27017, 'db': 'spider_py'}, 'es_addr': {"es_host": ("172.26.88.232",)}, 'redis':{'redis_nodes':[{"host": "127.0.0.1", "port": "6601"},{"host": "127.0.0.1", "port": "6602"},{"host": "127.0.0.1", "port": "6603"},{"host": "127.0.0.1", "port": "6604"},{"host": "127.0.0.1", "port": "6605"},{"host": "127.0.0.1", "port": "6606"},]}}
    else:
        run_evn_dict = {'mongo': {'host': '172.17.108.83', 'port': 27017, 'db': 'spider_py'}, 'es_addr': {
            'es_host': ("172.17.108.77", "172.17.108.78", "172.17.108.79")},
            'redis': {'redis_nodes': [{"host": "172.17.108.80", "port": "8000"},
                                      {"host": "172.17.108.80", "port": "8001"},
                                      {"host": "172.17.108.80", "port": "8002"},
                                      {"host": "172.17.108.80", "port": "8003"},
                                      {"host": "172.17.108.80", "port": "8004"},
                                      {"host": "172.17.108.80", "port": "8005"},
                                      {"host": "172.17.108.80", "port": "8006"},
                                      {"host": "172.17.108.82", "port": "8000"},
                                      {"host": "172.17.108.82", "port": "8001"},
                                      {"host": "172.17.108.82", "port": "8002"},
                                      {"host": "172.17.108.82", "port": "8003"},
                                      {"host": "172.17.108.82", "port": "8004"},
                                      {"host": "172.17.108.82", "port": "8005"},
                                      {"host": "172.17.108.82", "port": "8006"},
                                      {"host": "172.17.108.82", "port": "8007"},
                                      {"host": "172.17.108.71", "port": "8000"},
                                      {"host": "172.17.108.71", "port": "8001"},
                                      {"host": "172.17.108.71", "port": "8002"},
                                      {"host": "172.17.108.71", "port": "8003"},
                                      {"host": "172.17.108.71", "port": "8004"},
                                      {"host": "172.17.108.71", "port": "8005"},
                                      {"host": "172.17.108.71", "port": "8006"},
                                      {"host": "172.17.108.71", "port": "8007"},
                                     ]}}
    return run_evn_dict