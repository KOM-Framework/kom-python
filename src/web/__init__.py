from ... import env_file_content

# Selenium web driver configuration
element_load_time = env_file_content['element_load_time']
iframe_load_time = env_file_content['iframe_load_time']
http_request_wait_time = env_file_content['http_request_wait_time']
page_load_time = env_file_content['page_load_time']
retry_delay = env_file_content['retry_delay']

# Selenium Hub configurations
remote_execution = env_file_content['remote_execution'] == "True"
hub_ip = env_file_content['hub_ip']
hub_port = env_file_content['hub_port']

# Execution configurations
multi_application_mode = env_file_content['multi_application_mode'] == "True"
