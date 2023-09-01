import yaml
from nacos_service import register_nacos


def read_config():
    with open("config.yml", 'r') as stream:
        return yaml.safe_load(stream)


def init_config():
    yml_data = read_config()
    register_nacos(yml_data)
