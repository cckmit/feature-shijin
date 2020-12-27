
# dev; test; prod
run_evn = 'dev'

def get_run_env_dict():
    run_evn_dict = {}
    if 'dev' == run_evn:
        run_evn_dict = {'mongo': {'host': '127.0.0.1', 'port': 27017, 'db': 'spider_py'}, 'es_addr': {"es_host": ("123.56.187.45",)}, 'redis':{'redis_nodes':[{"host":"192.168.1.136","port":"8000"},{"host":"192.168.1.136","port":"8001"},{"host":"192.168.1.136","port":"8002"},{"host":"192.168.1.136","port":"8003"},{"host":"192.168.1.136","port":"8004"},{"host":"192.168.1.136","port":"8005"},]}}
    elif 'test' == run_evn:
        run_evn_dict = {'mongo': {'host': '127.0.0.1', 'port': 27017, 'db': 'spider_py'}, 'es_addr': {"es_host": ("123.56.187.45",)}, 'redis':{'redis_nodes':[{"host": "172.24.56.160", "port": "8000"},{"host": "172.24.56.160", "port": "8001"},{"host": "172.24.56.160", "port": "8002"},{"host": "172.24.56.160", "port": "8003"},{"host": "172.24.56.160", "port": "8004"},{"host": "172.24.56.160", "port": "8005"},]}}
    else:
        run_evn_dict = {'mongo': {'host': '127.0.0.1', 'port': 27020, 'db': 'spider_py'}, 'es_addr': {
            'es_host': ("10.27.223.106", "10.29.130.193", "10.144.112.79", "172.17.108.73", "172.17.108.74")},
            'redis': {'redis_nodes': [{"host": "10.66.205.48", "port": "8000"},
                                                  {"host": "10.66.205.48", "port": "8001"},
                                                  {"host": "10.66.205.48", "port": "8002"},
                                                  {"host": "10.66.205.48", "port": "8003"},
                                                  {"host": "10.66.205.48", "port": "8004"},
                                                  {"host": "10.66.205.48", "port": "8005"},
                                                  {"host": "10.66.205.48", "port": "8006"},
                                                  {"host": "172.17.108.71", "port": "8000"},
                                                  {"host": "172.17.108.71", "port": "8001"},
                                                  {"host": "172.17.108.71", "port": "8002"},
                                                  {"host": "172.17.108.71", "port": "8003"},
                                                  {"host": "172.17.108.71", "port": "8004"},
                                                  {"host": "172.17.108.71", "port": "8005"},
                                                  {"host": "172.17.108.71", "port": "8006"},
                                                  {"host": "172.17.108.71", "port": "8007"},
                                                  {"host": "10.27.217.22", "port": "8000"},
                                                  {"host": "10.27.217.22", "port": "8001"},
                                                  {"host": "10.27.217.22", "port": "8002"},
                                                  {"host": "10.27.217.22", "port": "8003"},
                                                  {"host": "10.27.217.22", "port": "8004"},
                                                  {"host": "10.27.217.22", "port": "8005"},
                                                  {"host": "10.27.217.22", "port": "8006"},
                                                  {"host": "10.27.217.22", "port": "8007"},

                                      ]}}
    return run_evn_dict