# coding=utf-8
import os
import Kit
import pymysql
import logging
import sentry_sdk
from flask import Flask
from flask import request
from flask_cors import CORS
from Config import get_config
from dbutils.pooled_db import PooledDB
from sentry_sdk.integrations.flask import FlaskIntegration

# 获取配置
app_config = get_config()
base_path = os.path.split(os.path.abspath(__file__))[0]

# Sentry
sentry_sdk.init(
    dsn=app_config['SENTRY']['dsn'],
    integrations=[FlaskIntegration()],
    environment=app_config["RUN_ENV"]
)

# 初始化应用
app = Flask(__name__)
app.config.from_mapping(app_config)

# 服务日志
file_logger = logging.getLogger('file_log')
file_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(filename='./log/run.log', encoding="utf-8")
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

# 初始化连接池
for key in app.config.get('POOL').keys():
    app.config.get('POOL')[key] = int(app.config.get('POOL')[key])
app.config.get('MYSQL')["port"] = int(app.config.get('MYSQL')["port"])
pool_config = app.config.get('POOL')
mysql_config = app.config.get('MYSQL')
app.mysql_pool = PooledDB(creator=pymysql, **mysql_config, **pool_config)

# 初始化路由
from Demo import demo_blue

app.register_blueprint(demo_blue, url_prefix='/demo')
CORS(app, supports_credentials=True, resources={r"/*": {"origins": app_config["BASE"]["cors_host"].split(",")}})


@app.route('/')
def hello_world():
    return Kit.common_rsp("Hello, world!")


@app.route('/generate_204')
def network_test():
    return str("success"), 204


@app.route('/debug/sentry')
def sentry_debug():
    app.logger.info("[DEBUG]Test sentry: {}".format(1 / 0))
    return Kit.common_rsp("DEBUG")


@app.errorhandler(400)
def http_forbidden(msg):
    app.logger.warning("{}: <HTTP 400> {}".format(request.url, msg))
    return Kit.common_rsp("Bad Request", status='Bad Request')


@app.errorhandler(403)
def http_forbidden(msg):
    return Kit.common_rsp(str(msg)[15:], status='Forbidden')


@app.errorhandler(404)
def http_not_found(msg):
    return Kit.common_rsp(str(msg)[15:], status='Not Found')


@app.errorhandler(500)
def service_error(msg):
    app.logger.error("{}: <HTTP 400> {}".format(request.url, msg))
    return Kit.common_rsp(str(msg)[15:], status='Internal Server Error')


if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

if __name__ == '__main__':
    app.logger.setLevel(logging.DEBUG)
    app.run(host='0.0.0.0', port=12880, debug=True)
    exit()
