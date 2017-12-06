import os
import json

config_file = 'kom_framework/src/resources/.kom.config.json'
env_file_content = json.load(open(os.path.abspath(config_file)))
