from kom_framework import env_file_content
from ...utils.proxy import Proxy
from ...utils import proxy_ip

capabilities = env_file_content['driver_configurations']
capabilities['loggingPrefs'] = {'browser': 'ALL'}

if proxy_ip:
    proxy_url = Proxy.get_url()
    capabilities['proxy'] = {
        "ftpProxy": proxy_url,
        "sslProxy": proxy_url,
        "httpProxy": proxy_url,
        "class": "org.openqa.selenium.Proxy",
        "autodetect": "False",
        "noProxy": "None",
        "proxyType": "MANUAL"
    }
