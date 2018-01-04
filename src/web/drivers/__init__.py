from kom_framework import env_file_content
from ...utils import proxy_ip, proxy_port

capabilities = env_file_content['driver_configurations']

if proxy_ip:
    capabilities['proxy'] = {
        "ftpProxy": "%s:%s" % (proxy_ip, proxy_port),
        "sslProxy": "%s:%s" % (proxy_ip, proxy_port),
        "httpProxy": "%s:%s" % (proxy_ip, proxy_port),
        "class": "org.openqa.selenium.Proxy",
        "autodetect": "False",
        "noProxy": "None",
        "proxyType": "MANUAL"
    }
