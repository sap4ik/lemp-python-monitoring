from flask import Flask, jsonify
import pymysql
import logging
from logging.handlers import RotatingFileHandler
import os
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

# Настройка логирования
log_dir = '/var/www/python-app/logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

file_handler = RotatingFileHandler(f'{log_dir}/app.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Flask application started')

# Метрики для Prometheus
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.0')

DB_CONFIG = {
    'host': 'localhost',
    'user': 'sap',
    'password': '1337',
    'database': 'mysql',
    'charset': 'utf8mb4'
}

@app.route('/')
def home():
    return jsonify({
        'message': 'Hello from sap, EN v 2.0',
        'status': 'cool',
        'creator': 'sap'
    })

@app.route('/db-test')
def db_test():
    try:
        connection = pymysql.connect(**DB_CONFIG)
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION();")
            version = cursor.fetchone()
        connection.close()
        return jsonify({
            'database': 'connected',
            'version': version[0] if version else 'unknown',
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'database': 'error',
            'message': str(e),
            'status': 'failed'
        }), 500

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/metrics')
def metrics_endpoint():
    from prometheus_flask_exporter import PrometheusMetrics
    return PrometheusMetrics(app).export()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
