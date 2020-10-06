from kom_framework.src.web import appium_remote, appium_port, appium_cookies, appium_platform


class AppiumForMac:

    @classmethod
    def generate_cookies(cls):
        cookies = []
        for k, v in appium_cookies.items():
            cookies.append({'name': k, 'value': v})
        return cookies

    @classmethod
    def get_capabilities(cls):
        capabilities = {'platform': appium_platform, 'cookies': cls.generate_cookies()}
        return capabilities


class AppiumDriver:

    hub_link = f'http://{appium_remote}:{appium_port}/wd/hub'

    @classmethod
    def get_remote_session(cls):
        capabilities = AppiumForMac.get_capabilities()
        from appium import webdriver
        driver = webdriver.Remote(
            command_executor=cls.hub_link,
            desired_capabilities=capabilities)
        return driver
