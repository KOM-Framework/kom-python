import json
import os
from urllib.parse import urlparse

from browsermobproxy import Server

from kom_framework.src.general import Log
from kom_framework.src.utils import proxy_port
from kom_framework.src.web import remote_execution, hub_ip


class Proxy:

    proxy = None
    server = None
    port = proxy_port
    path = 'browsermob-proxy/bin/browsermob-proxy'
    url = None

    @classmethod
    def start(cls):
        Log.info("Starting browsermob-proxy server")
        root = os.path.dirname(__file__)
        proxy_path = os.path.abspath(os.path.join(root, cls.path))
        cls.server = Server(proxy_path, options={"port": cls.port})
        cls.server.start()
        cls.proxy = cls.server.create_proxy()
        return cls.get_url()

    @classmethod
    def new_har(cls):
        if not cls.proxy:
            cls.start()
        cls.proxy.new_har(options={"captureHeaders": True, "captureContent": True})

    @classmethod
    def get_url(cls):
        if not cls.url:
            if not cls.proxy:
                cls.start()
            cls.url = urlparse(cls.proxy.proxy).path
            if remote_execution:
                cls.url = cls.url.replace('localhost', hub_ip)
        return cls.url

    @classmethod
    def get_har(cls):
        return cls.proxy.har

    @classmethod
    def stop(cls):
        if cls.server:
            Log.info('Closing browsermob-proxy server')
            cls.server.stop()
            cls.proxy = None
            cls.server = None

    @classmethod
    def write_har_to_file(cls, file, har=None):
        root = os.path.dirname(__file__)
        logo = os.path.abspath(os.path.join(root, file))
        file = open(logo, 'w+')
        if not har:
            har = cls.get_har()
        har_data = json.dumps(har, indent=4)
        file.write('onInputData(%s);' % har_data)
        file.close()
