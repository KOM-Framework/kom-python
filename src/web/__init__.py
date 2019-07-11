from ... import kom_config

# Selenium web driver configuration
element_load_time = kom_config['element_load_time']
iframe_load_time = kom_config['iframe_load_time']
http_request_wait_time = kom_config['http_request_wait_time']
page_load_time = kom_config['page_load_time']
retry_delay = kom_config['retry_delay']

# Selenium Hub configurations
remote_execution = kom_config['remote_execution'] == "True"
hub_ip = kom_config['hub_ip']
hub_port = kom_config['hub_port']
