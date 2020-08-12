from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from kom_framework.src.drivers import capabilities


class Chrome:

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


class FireFox:

    @classmethod
    def get_capabilities(cls, extensions=None):
        firefox_capabilities = DesiredCapabilities.FIREFOX.copy()
        firefox_capabilities["marionette"] = False
        return firefox_capabilities

    @classmethod
    def get_session(cls, driver_capabilities):
        from webdriver_manager.firefox import GeckoDriverManager
        if 'enableVNC' in driver_capabilities:
            driver_capabilities.pop('enableVNC')
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(),
                                   capabilities=driver_capabilities)
        return driver


class InternetExplorer:

    @classmethod
    def get_capabilities(cls, extensions=None):
        return DesiredCapabilities.INTERNETEXPLORER.copy()

    @classmethod
    def get_session(cls, driver_capabilities):
        from webdriver_manager.microsoft import IEDriverManager
        capabilities.pop('platform', "windows")
        driver_capabilities = {**cls.get_capabilities(), **capabilities}
        driver = webdriver.Ie(executable_path=IEDriverManager(version="3.9.0", os_type="win32").install(),
                              capabilities=driver_capabilities)
        return driver


class Opera:

    @classmethod
    def get_capabilities(cls, extensions=None):
        return DesiredCapabilities.OPERA

    @classmethod
    def get_session(cls, driver_capabilities):
        raise Exception('Not IMPLEMENTED FOR LOCAL EXECUTION')