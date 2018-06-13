from kom_framework import env_file_content

capabilities = env_file_content['driver_configurations']
capabilities['loggingPrefs'] = {'browser': 'ALL'}
