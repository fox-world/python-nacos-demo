import datetime
import yaml
from flask import Flask

import config.nacos as cn
import config.settings as cs

app = Flask(__name__)

with app.app_context():
    cs.init_config()
    app.logger.info("=========flask start success===========")

if __name__ == '__main__':
    app.run()


@app.route('/')
def hello():
    result = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result += '\tHello flask!'
    return result


@app.route('/config')
def read_config():
    config = cn.read_config(cn.NACOS_CLIENT, "training_datasource_config.yml", "orienlink")
    return yaml.safe_load(config)
