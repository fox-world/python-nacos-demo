import nacos
import time
import threading
import logging

from flask import current_app


class NacosServer:

    def __init__(self, server_port, server_address):
        self.server_port = server_port
        self.server_address = server_address


class NacosService:

    def __init__(self, namespace, cluster_name, group_name, service_name, service_address):
        self.namespace = namespace
        self.cluster_name = cluster_name
        self.group_name = group_name
        self.service_name = service_name
        self.service_address = service_address


NACOS_SERVER = None
NACOS_SERVICE = None
NACOS_CLIENT = None


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

    global NACOS_CLIENT
    NACOS_CLIENT = nacos.NacosClient(server_address, namespace=namespace)
    NACOS_CLIENT.add_naming_instance(service_name, service_address, port, cluster_name, group_name=group_name)
    current_app.logger.info("=========register nacos success===========")

    thread = threading.Thread(target=send_heartbeat, name="send_heartbeat_threads",
                              args=(NACOS_CLIENT, service_name, service_address, port, cluster_name, group_name))
    thread.start()


def send_heartbeat(client, service_name, ip, port, cluster_name, group_name):
    logger = logging.getLogger(__name__)
    while True:
        response = client.send_heartbeat(service_name, ip, port, cluster_name=cluster_name, group_name=group_name)
        logger.info(response)
        time.sleep(5)


def read_config(client, data_id, group):
    config = client.get_config(data_id, group, no_snapshot=True)
    return config
