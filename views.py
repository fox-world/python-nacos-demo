import datetime
import nacos_service as ns
import yaml

from flask import request


def hello():
    result = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result += '\tHello flask!'
    return result


def get_config():
    result = dict(time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    config = ns.get_config("training_datasource_config.yml", "orienlink")
    result['config'] = yaml.safe_load(config)
    return result


def get_instance():
    service_name = request.args.get("service_name")
    result = ns.get_instance(service_name)
    return result


def invoke_instance():
    service = request.args.get("service")
    method = request.args.get("method")
    response = ns.invoke_instance(service, method)
    result = dict(time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    result['data'] = response
    return result
