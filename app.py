import datetime
from flask import Flask

from config.settings import init_config

app = Flask(__name__)

with app.app_context():
    init_config()
    app.logger.info("=========flask start success===========")

if __name__ == '__main__':
    app.run()


@app.route('/')
def hello():
    result = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result += '\tHello flask!'
    return result
