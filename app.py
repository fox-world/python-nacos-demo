import datetime
import yaml
from flask import Flask, request

import nacos_service as cn
import logging
import sys

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
stdout = logging.StreamHandler(sys.stdout)
stdout.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s"))
logger.addHandler(stdout)

app = Flask(__name__)

with app.app_context():
    with open("config.yml", 'r') as stream:
        yaml_data = yaml.safe_load(stream)
    cn.register_nacos(yaml_data)
    app.logger.info("=========flask start success===========")

if __name__ == '__main__':
    app.run()


@app.route('/')
def hello():
    result = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result += '\tHello flask!'
    return result


@app.route('/config')
def get_config():
    result = dict(time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    config = cn.get_config("training_datasource_config.yml", "orienlink")
    result['config'] = yaml.safe_load(config)
    return result


@app.route("/instances")
def get_instance():
    service_name = request.args.get("service_name")
    result = cn.get_instance(service_name)
    return result


@app.route("/invoke")
def invoke_instance():
    service = request.args.get("service")
    method = request.args.get("method")
    response = cn.invoke_instance(service, method)
    result = dict(time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    result['data'] = response
    return result
