import datetime
from flask import Flask

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
    print(cs.NACOS_SERVER.server_address)
    print(cs.NACOS_SERVICE.namespace)
    result = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result += '\tHello flask!'
    return result
