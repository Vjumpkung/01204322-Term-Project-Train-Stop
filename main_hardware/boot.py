import sys

# if you add folder please append folder/directory name here
sys.path.append("config")
sys.path.append("sensors")
sys.path.append("mqtt")
sys.path.append("network")
sys.path.append("user_lib")  # file library from user

from wifi_connect import do_connect
from load_config import SSID, PASSWORD

do_connect(SSID, PASSWORD)
