import os
import json

if os.environ.get("KOM_CONFIG_STRING"):
    kom_config = json.loads(os.environ.get("KOM_CONFIG_STRING"))
else:
    config_file = 'kom_framework/resources/.kom.config.json'
    kom_config = json.load(open(os.path.abspath(config_file)))

js_waiter_file = 'kom_framework/resources/.http.waiter.js'
