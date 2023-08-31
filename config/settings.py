import yaml
from config.log import init_log
from config.nacos import register_nacos


def read_config():
    with open("config.yml", 'r') as stream:
        return yaml.safe_load(stream)


def init_config():
    init_log()
    yml_data = read_config()
    register_nacos(yml_data)
