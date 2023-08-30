from logging.config import dictConfig
from flask import current_app

import nacos
import yaml
import time
import threading


def read_config():
    with open("config.yml", 'r') as stream:
        return yaml.safe_load(stream)


def init_log():
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default'
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    })


def register_nacos(yml_data):
    server_address = yml_data['nacos']['server_address']
    namespace = yml_data['nacos']['namespace']
    client = nacos.NacosClient(server_address, namespace=namespace)

    ip = yml_data['nacos']['service_address']
    port = yml_data['nacos']['server_port']
    cluster_name = yml_data['nacos']['cluster_name']
    service_name = yml_data['nacos']['service_name']
    group_name = yml_data['nacos']['group_name']
    client.add_naming_instance(service_name, ip, port, cluster_name, group_name=group_name)
    current_app.logger.info("=========register nacos success===========")

    thread = threading.Thread(target=send_heartbeat, name="send_heartbeat_threads",
                              args=(client, service_name, ip, port, cluster_name, group_name))
    thread.start()


def send_heartbeat(client, service_name, ip, port, cluster_name, group_name):
    while True:
        client.send_heartbeat(service_name, ip, port, cluster_name=cluster_name, group_name=group_name)
        time.sleep(5)


def init_config():
    yml_data = read_config()
    init_log()
    register_nacos(yml_data)
