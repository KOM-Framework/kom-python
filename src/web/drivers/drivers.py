import os
from abc import ABCMeta, abstractmethod

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import Options as ChromeOptions

from kom_framework.src.utils import use_proxy
from kom_framework.src.utils.proxy import Proxy
from kom_framework.src.web import hub_ip, remote_execution, headless_mode


class Driver:

    __metaclass__ = ABCMeta

    @classmethod
    @abstractmethod
    def get_session(cls):
        pass

    @classmethod
    @abstractmethod
    def get_capabilities(cls, extension=None):
        pass

    def get_remove_session(self, extension=None):
        driver = webdriver.Remote(
            command_executor=hub_ip,
            desired_capabilities=self.get_capabilities(extension)
        ).maximize_window()
        return driver

    @classmethod
    def get(cls, extension=None):
        if remote_execution:
            return cls.get_remove_session(extension)
        else:
            return cls.get_session(extension)


class Chrome(Driver):

    @classmethod
    def get_session(cls, extension=None):
        from webdriver_manager.chrome import ChromeDriverManager
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),
                                  desired_capabilities=cls.get_capabilities(extension))
        return driver

    @classmethod
    def get_capabilities(cls, extension=None):
        chrome_options = ChromeOptions()
        chrome_options.add_experimental_option('prefs', {
            'credentials_enable_service': False,
            'profile': {
                'password_manager_enabled': False
            }
        })
        if extension:
            root = os.path.dirname(__file__)
            extension_path = os.path.abspath(os.path.join(root, extension))
            chrome_options.add_extension(extension_path)
        if headless_mode:
            chrome_options.add_argument('headless')
            chrome_options.add_argument('--no-sandbox')
        capabilities = chrome_options.to_capabilities()
        if use_proxy:
            proxy_url = Proxy.get_url()
            capabilities['proxy'] = {
                "httpProxy": proxy_url,
                "ftpProxy": proxy_url,
                "sslProxy": proxy_url,
                "noProxy": None,
                "proxyType": "MANUAL",
                "class": "org.openqa.selenium.Proxy",
                "autodetect": False
            }
        capabilities['loggingPrefs'] = {'browser': 'ALL'}
        return capabilities
