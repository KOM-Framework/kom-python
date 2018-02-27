import base64

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from ...web.drivers import capabilities
from ...web import hub_ip, remote_execution, hub_port


class Driver:

    def __init__(self, extensions=None):
        self.extensions = extensions

    hub_link = 'http://%s:%s/wd/hub' % (hub_ip, hub_port)

    def get_remove_session(self):
        if self.extensions:
            for extension in self.extensions:
                Chrome.add_extension(extension)
        driver = webdriver.Remote(
            command_executor=self.hub_link,
            desired_capabilities=capabilities)
        return driver

    def get_local_session(self):
        if capabilities['browserName'] == 'firefox':
            driver_type = FireFox
        elif capabilities['browserName'] == 'internet explorer':
            driver_type = InternetExplorer
        else:
            driver_type = Chrome
        if self.extensions:
            for extension in self.extensions:
                driver_type.add_extension(extension)
        return driver_type.get_session()

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
    def get_chrome_capabilities(cls):
        from selenium.webdriver.chrome.webdriver import Options as ChromeOptions
        chrome_options = ChromeOptions()
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
    def get_session(cls):
        from webdriver_manager.chrome import ChromeDriverManager
        driver_capabilities = {**cls.get_chrome_capabilities(), **capabilities}
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),
                                  desired_capabilities=driver_capabilities)
        return driver

    @staticmethod
    def add_extension(extension_path):
        file_ = open(extension_path, 'rb')
        # Should not use base64.encodestring() which inserts newlines every
        # 76 characters (per RFC 1521).  Chromedriver has to remove those
        # unnecessary newlines before decoding, causing performance hit.
        capabilities["goog:chromeOptions"]['extensions'] = [base64.b64encode(file_.read()).decode('UTF-8')]
        file_.close()


class FireFox(Driver):

    @classmethod
    def get_firefox_capabilities(cls):
        firefox_capabilities = DesiredCapabilities.FIREFOX.copy()
        firefox_capabilities['loggingPrefs'] = {'browser': 'ALL'}
        return firefox_capabilities

    @classmethod
    def get_session(cls):
        from webdriver_manager.firefox import GeckoDriverManager
        driver_capabilities = {**cls.get_firefox_capabilities(), **capabilities}
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
    def get_ie_capabilities(cls):
        return DesiredCapabilities.INTERNETEXPLORER.copy()

    @classmethod
    def get_session(cls):
        from webdriver_manager.microsoft import IEDriverManager
        capabilities.pop('platform')
        driver_capabilities = {**cls.get_ie_capabilities(), **capabilities}
        driver = webdriver.Ie(executable_path=IEDriverManager(os_type="win32").install(),
                              capabilities=driver_capabilities)
        return driver
