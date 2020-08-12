from ... import kom_config

# Selenium web driver configuration
element_load_time = kom_config['element_load_time']
iframe_load_time = kom_config['iframe_load_time']
http_request_wait_time = kom_config['http_request_wait_time']
page_load_time = kom_config['page_load_time']
retry_delay = kom_config['retry_delay']

# Selenium Hub configurations
remote_execution = kom_config['web_driver_configurations']['remote_execution'] == "True"
hub_ip = kom_config['web_driver_configurations']['hub_ip']
hub_port = kom_config['web_driver_configurations']['hub_port']

# Appium configuration
appium_platform = kom_config['appium_configurations']['platform']
appium_remote = kom_config['appium_configurations']['remote']
appium_port = kom_config['appium_configurations']['port']
appium_cookies = kom_config['appium_configurations']['cookies']
