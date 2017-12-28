from selenium import webdriver
from ...web import hub_ip, remote_execution, hub_port


class Driver:

    hub_link = 'http://%s:%s/wd/hub' % (hub_ip, hub_port)

    def get_remove_session(self, desired_capabilities):
        driver = webdriver.Remote(
            command_executor=self.hub_link,
            desired_capabilities=desired_capabilities)
        driver.set_window_size(1920, 1080)
        return driver

    def create_session(self, desired_capabilities):
        if remote_execution:
            driver = self.get_remove_session(desired_capabilities)
        else:
            from webdriver_manager.chrome import ChromeDriverManager
            driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),
                                      desired_capabilities=desired_capabilities)
        driver.set_window_size(1920, 1080)
        return driver


class Chrome(Driver):

    @classmethod
    def get_session(cls, desired_capabilities):
        from webdriver_manager.chrome import ChromeDriverManager
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),
                                  desired_capabilities=desired_capabilities)

        return driver


class FireFox(Driver):

    @classmethod
    def get_session(cls, desired_capabilities):
        from webdriver_manager.firefox import GeckoDriverManager
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(),
                                   capabilities=desired_capabilities)
        return driver
