import os
import json

if os.environ.get("KOM_CONFIG_STRING"):
    env_file_content = json.loads(os.environ.get("KOM_CONFIG_STRING"))
elif os.environ.get("KOM_CONFIG"):
    if os.environ.get("KOM_CONFIG").lower()=="ie":
        config_file = 'kom_framework/src/resources/.kom.config_ie.json'
        env_file_content = json.load(open(os.path.abspath(config_file)))
else:
    config_file = 'kom_framework/src/resources/.kom.config.json'
    env_file_content = json.load(open(os.path.abspath(config_file)))

retry_failed = env_file_content['retry_failed']
js_waiter_file = 'kom_framework/src/resources/.http.waiter.js'
