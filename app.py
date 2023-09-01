import datetime
import yaml
from flask import Flask, request
import log
import nacos_service as ns

app = Flask(__name__)

with app.app_context():
    with open("config.yml", 'r') as stream:
        yaml_data = yaml.safe_load(stream)

    ns.register_nacos(yaml_data)

    logger = log.get_logger(__name__)
    logger.info("=========flask start success===========")

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
    config = ns.get_config("training_datasource_config.yml", "orienlink")
    result['config'] = yaml.safe_load(config)
    return result


@app.route("/instances")
def get_instance():
    service_name = request.args.get("service_name")
    result = ns.get_instance(service_name)
    return result


@app.route("/invoke")
def invoke_instance():
    service = request.args.get("service")
    method = request.args.get("method")
    response = ns.invoke_instance(service, method)
    result = dict(time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    result['data'] = response
    return result
