from logging.config import dictConfig
import nacos
from flask import current_app


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


def register_nacos():
    service_name = "flask-app"
    ip = "10.30.65.49"
    port = "8858"
    cluster_name = "default"

    SERVER_ADDRESSES = "10.10.2.98:8858"
    NAMESPACE = "e1c19595-0757-4231-89cb-19ea2db3bd8d"

    client = nacos.NacosClient(SERVER_ADDRESSES, namespace=NAMESPACE)

    client.add_naming_instance(service_name, ip, port, cluster_name, group_name="dev-1")

    current_app.logger.info("=========register nacos success===========")


def init_config():
    init_log()
    register_nacos()
