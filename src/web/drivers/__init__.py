from kom_framework import env_file_content
from . import drivers

# capabilities = env_file_content['driver_configurations']

capabilities = {
    # "proxy": {
    #     "ftpProxy": "35.202.136.79:8089",
    #     "sslProxy": "35.202.136.79:8089",
    #     "httpProxy": "35.202.136.79:8089",
    #     "class": "org.openqa.selenium.Proxy",
    #     "autodetect": "False",
    #     "noProxy": "None",
    #     "proxyType": "MANUAL"
    # },
    "browserName": "chrome",
    "platform": "ANY",
    "version": "",
    "goog:chromeOptions": {
        "prefs": {
            "credentials_enable_service": "False",
            "profile": {
                "password_manager_enabled": "False"
            }
        },
        # "extensions": [],
        # "args": [
        #     "--headless",
        #     "--no-sandbox"
        # ]
    },
    "loggingPrefs": {
        "browser": "ALL"
    }
}
