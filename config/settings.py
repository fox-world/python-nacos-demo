import nacos
import yaml
import time
import threading
import logging

from flask import current_app
from config.nacos import NacosServer, NacosService
from config.log import init_log


def read_config():
    with open("config.yml", 'r') as stream:
        return yaml.safe_load(stream)


NACOS_SERVER = None
NACOS_SERVICE = None


def register_nacos(yml_data):
    # 服务器配置
    port = yml_data['nacos']['server_port']
    server_address = yml_data['nacos']['server_address']
    global NACOS_SERVER
    NACOS_SERVER = NacosServer(port, server_address)

    # 调用方配置
    namespace = yml_data['nacos']['namespace']
    service_address = yml_data['nacos']['service_address']
    cluster_name = yml_data['nacos']['cluster_name']
    service_name = yml_data['nacos']['service_name']
    group_name = yml_data['nacos']['group_name']
    global NACOS_SERVICE
    NACOS_SERVICE = NacosService(namespace, cluster_name, group_name, service_name, service_address)

    client = nacos.NacosClient(server_address, namespace=namespace)
    client.add_naming_instance(service_name, service_address, port, cluster_name, group_name=group_name)
    current_app.logger.info("=========register nacos success===========")

    thread = threading.Thread(target=send_heartbeat, name="send_heartbeat_threads",
                              args=(client, service_name, service_address, port, cluster_name, group_name))
    thread.start()


def send_heartbeat(client, service_name, ip, port, cluster_name, group_name):
    logger = logging.getLogger(__name__)
    while True:
        response = client.send_heartbeat(service_name, ip, port, cluster_name=cluster_name, group_name=group_name)
        logger.info(response)
        time.sleep(5)


def init_config():
    yml_data = read_config()
    init_log()
    register_nacos(yml_data)
