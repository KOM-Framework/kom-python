from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from ...web.drivers import capabilities
from ...web import hub_ip, remote_execution, hub_port


class Driver:

    def __init__(self, extensions=None):
        self.extensions = extensions

    hub_link = 'http://%s:%s/wd/hub' % (hub_ip, hub_port)

    @staticmethod
    def get_driver_type(browser_name):
        if browser_name == 'firefox':
            return FireFox
        elif browser_name == 'internet explorer':
            return InternetExplorer
        else:
            return Chrome

    def get_remove_session(self):
        driver_type = self.get_driver_type(capabilities['browserName'])
        driver_capabilities = {**driver_type.get_capabilities(self.extensions), **capabilities}
        driver = webdriver.Remote(
            command_executor=self.hub_link,
            desired_capabilities=driver_capabilities)
        return driver

    def get_local_session(self):
        driver_type = self.get_driver_type(capabilities['browserName'])
        driver_capabilities = {**driver_type.get_capabilities(self.extensions), **capabilities}
        return driver_type.get_session(driver_capabilities)

    def create_session(self):
        if remote_execution:
            driver = self.get_remove_session()
        else:
            driver = self.get_local_session()
        width = int(capabilities['browserSize'].split('x')[0])
        height = int(capabilities['browserSize'].split('x')[1])
        driver.set_window_size(width, height)
        driver.set_window_position(0, 0)
        return driver


class Chrome(Driver):

    @classmethod
    def get_capabilities(cls, extensions=None):
        from selenium.webdriver.chrome.webdriver import Options as ChromeOptions
        chrome_options = ChromeOptions()
        if extensions:
            for extension in extensions:
                chrome_options.add_extension(extension)
        chrome_options.add_experimental_option('prefs', {
            'credentials_enable_service': False,
            'profile': {
                'password_manager_enabled': False
            }
        })
        chrome_capabilities = chrome_options.to_capabilities()
        chrome_capabilities['loggingPrefs'] = {'browser': 'ALL'}
        return chrome_capabilities

    @classmethod
    def get_session(cls, driver_capabilities):
        from webdriver_manager.chrome import ChromeDriverManager
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),
                                  desired_capabilities=driver_capabilities)
        return driver


class FireFox(Driver):

    @classmethod
    def get_capabilities(cls, extensions=None):
        firefox_capabilities = DesiredCapabilities.FIREFOX.copy()
        firefox_capabilities['loggingPrefs'] = {'browser': 'ALL'}
        return firefox_capabilities

    @classmethod
    def get_session(cls):
        from webdriver_manager.firefox import GeckoDriverManager
        driver_capabilities = {**cls.get_capabilities(), **capabilities}
        driver_capabilities.pop('browserSize')
        driver_capabilities.pop('version')
        driver_capabilities.pop('platform')
        if 'enableVNC' in driver_capabilities:
            driver_capabilities.pop('enableVNC')
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(),
                                   capabilities=driver_capabilities)
        return driver


class InternetExplorer(Driver):

    @classmethod
    def get_capabilities(cls, extensions=None):
        return DesiredCapabilities.INTERNETEXPLORER.copy()

    @classmethod
    def get_session(cls):
        from webdriver_manager.microsoft import IEDriverManager
        capabilities.pop('platform')
        driver_capabilities = {**cls.get_capabilities(), **capabilities}
        driver = webdriver.Ie(executable_path=IEDriverManager(os_type="win32").install(),
                              capabilities=driver_capabilities)
        return driver
