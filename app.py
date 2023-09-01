import yaml
from flask import Flask
import log
import nacos_service as ns
import views

app = Flask(__name__)

# 程序启动后的初始化工作
with app.app_context():
    with open("config.yml", 'r') as stream:
        yaml_data = yaml.safe_load(stream)

    ns.register_nacos(yaml_data)

    logger = log.get_logger(__name__)
    logger.info("=========flask start success===========")

if __name__ == '__main__':
    app.run()

app.add_url_rule('/', view_func=views.hello)
app.add_url_rule('/config', view_func=views.get_config)
app.add_url_rule('/instances', view_func=views.get_instance)
app.add_url_rule('/invoke', view_func=views.invoke_instance)
