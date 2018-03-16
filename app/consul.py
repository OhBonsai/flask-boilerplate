# coding=utf-8
# Created by OhBonsai at 2018/3/15
from flask_restful import Resource
from flask import Blueprint
from flask_restful import Api
from flask_consulate import Consul


def register_consul(app):
    if 'CONSUL_SERVER_HOST' not in app.config:
        return app

    host_ip = app.config['SERVER_HOST'] or get_ip_address(app.config['HOST_ADAPTER'])
    consul = Consul(app=app,
                    consul_host=app.config['CONSUL_SERVER_HOST'],
                    consul_port=app.config['CONSUL_SERVER_PORT'])
    consul.apply_remote_config(namespace=app.config['CONSUL_NAMESPACE'])
    consul.register_service(
        name=app.config['CONSUL_SERVICE_NAME'],
        interval=app.config['CONSUL_REGISTER_INTERVAL'],
        tags=app.config['CONSUL_REGISTER_TAGS'],
        port=app.config['SERVER_PORT'],
        address=host_ip,
        httpcheck='http://{host}:{port}/health'.format(host=host_ip, port=app.config['SERVER_PORT'])
    )

    register_health_check_api(app)
    return app


def register_health_check_api(app):
    common_bp = Blueprint('common', __name__)
    common_api = Api(common_bp, catch_all_404s=True)
    common_api.add_resource(AppHealthResource, '/health')
    app.register_blueprint(common_bp)


class AppHealthResource(Resource):
    def get(self):
        """
        This function is used to say current status to the Consul.
        Format: https://www.consul.io/docs/agent/checks.html

        :return: Empty response with status 200, 429 or 500
        """
        # TODO: implement any other checking logic.
        return ''


def get_ip_address(ifname):
    import socket
    try:
        import fcntl
    except ImportError:  # In windows
        return "127.0.0.1"

    import struct
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip = socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,   # SIOCGIFADDR
            struct.pack('256s', ifname[:15].encode('utf-8'))
        )[20:24])
        return ip
    finally:
        return "127.0.0.1"

