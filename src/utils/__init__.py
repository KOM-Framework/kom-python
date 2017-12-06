from kom_framework import env_file_content

use_proxy = env_file_content['use_proxy'] == "True"
proxy_port = env_file_content['proxy_port']
video_recording = env_file_content['video_recording'] == "True"
