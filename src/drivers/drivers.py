from selenium import webdriver

from .web_drivers import Chrome, InternetExplorer, Opera, FireFox
from kom_framework.src.drivers import capabilities
from kom_framework.src.web import hub_ip, remote_execution, hub_port
from ..general import Log


class Driver:

    def __init__(self, extensions=None):
        self.extensions = extensions

    hub_link = f'http://{hub_ip}:{hub_port}/wd/hub'

    @staticmethod
    def get_driver_type(driver_name):
        if driver_name == 'firefox':
            return FireFox
        elif driver_name == 'opera':
            return Opera
        elif driver_name == 'internet explorer':
            return InternetExplorer
        else:
            return Chrome

    def get_driver_capabilities(self):
        driver_type = self.get_driver_type(capabilities['browserName'])
        driver_capabilities = driver_type.get_capabilities(self.extensions)
        driver_capabilities['version'] = capabilities['version']
        return driver_capabilities

    def get_remote_session(self):
        driver = webdriver.Remote(
            command_executor=self.hub_link,
            desired_capabilities=self.get_driver_capabilities())
        return driver

    def get_local_session(self):
        driver_type = self.get_driver_type(capabilities['browserName'])
        return driver_type.get_session(self.get_driver_capabilities())

    def create_session(self):
        if remote_execution:
            driver = self.get_remote_session()
        else:
            driver = self.get_local_session()
        width = int(capabilities['browserSize'].split('x')[0])
        height = int(capabilities['browserSize'].split('x')[1])
        driver.set_window_size(width, height)
        driver.set_window_position(0, 0)
        Log.info(f'Created driver session for {driver.capabilities["browserName"]} '
                 f'v{driver.capabilities["browserVersion"]} browser')
        return driver
