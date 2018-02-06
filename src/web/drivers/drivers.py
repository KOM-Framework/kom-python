import base64

from selenium import webdriver

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
        driver.set_window_size(1920, 1080)
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
        driver.set_window_size(1024, 768)
        driver.set_window_position(0, 0)
        return driver


class Chrome(Driver):

    """
        chrome capabilities config example:
        "goog:chromeOptions": {
            "prefs": {
                "credentials_enable_service": "False",
                "profile": {
                    "password_manager_enabled": "False"
                }
            },
            "args": [
                "--headless",
                "--no-sandbox"
            ]
        }
    """

    @classmethod
    def get_session(cls):
        from webdriver_manager.chrome import ChromeDriverManager
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),
                                  desired_capabilities=capabilities)

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
    def get_session(cls):
        from webdriver_manager.firefox import GeckoDriverManager
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(),
                                   capabilities=capabilities)
        return driver


class InternetExplorer(Driver):

    @classmethod
    def get_session(cls):
        from webdriver_manager.microsoft import IEDriverManager
        driver = webdriver.Ie(executable_path=IEDriverManager().install(), capabilities=capabilities)
        return driver
