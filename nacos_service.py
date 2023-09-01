import nacos
import time
import threading
import logging
import requests
import json


class NacosServer:

    def __init__(self, server_port, server_address):
        self.server_port = server_port
        self.server_address = server_address


class NacosService:

    def __init__(self, namespace, group_name, service_name, service_address):
        self.namespace = namespace
        self.group_name = group_name
        self.service_name = service_name
        self.service_address = service_address


NACOS_SERVER = None
NACOS_SERVICE = None
NACOS_CLIENT = None

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def register_nacos(yml_data):
    # 服务器配置
    port = yml_data['nacos']['server_port']
    server_address = yml_data['nacos']['server_address']
    global NACOS_SERVER
    NACOS_SERVER = NacosServer(port, server_address)

    # 调用方配置
    namespace = yml_data['nacos']['namespace']
    service_address = yml_data['nacos']['service_address']
    service_name = yml_data['nacos']['service_name']
    group_name = yml_data['nacos']['group_name']
    global NACOS_SERVICE
    NACOS_SERVICE = NacosService(namespace, group_name, service_name, service_address)

    global NACOS_CLIENT
    NACOS_CLIENT = nacos.NacosClient(server_address, namespace=namespace)
    NACOS_CLIENT.add_naming_instance(service_name, service_address, port, group_name=group_name)
    logger.info("=========register nacos success===========")

    thread = threading.Thread(target=send_heartbeat, name="send_heartbeat_threads",
                              args=(NACOS_CLIENT, service_name, service_address, port, group_name))
    thread.start()


def send_heartbeat(client, service_name, ip, port, group_name):
    while True:
        client.send_heartbeat(service_name, ip, port, group_name=group_name)
        time.sleep(5)


def get_config(data_id, group):
    config = NACOS_CLIENT.get_config(data_id, group, no_snapshot=True)
    return config


def get_instance(service_name):
    namespace = NACOS_SERVICE.namespace
    group_name = NACOS_SERVICE.group_name
    instances = NACOS_CLIENT.list_naming_instance(service_name, namespace_id=namespace,
                                                  group_name=group_name,
                                                  healthy_only=True)
    return instances


def invoke_instance(service, method):
    instances = get_instance(service)
    ip = instances['hosts'][0]['ip']
    port = instances['hosts'][0]['port']
    url = "http://" + ip + ":" + str(port) + "/" + method
    response = requests.get(url).text
    return json.loads(response)
