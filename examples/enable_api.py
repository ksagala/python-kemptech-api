from python_kemptech_api import *

loadmaster_ip = ""
username = ""
password = ""

lm = LoadMaster(loadmaster_ip, username, password)
lm.enable_api()
print(lm['version'])
