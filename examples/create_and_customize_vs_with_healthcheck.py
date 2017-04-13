from python_kemptech_api import *

# Specify the LoadMaster connection credentials here:
loadmaster_ip = ""
username = ""
password = ""

lm = LoadMaster(loadmaster_ip, username, password)

# Create the Virtual Service
vs_ip = ""
vs_port = ""

vs = lm.create_virtual_service(vs_ip, vs_port, "tcp")
vs.save()

# Customize your VS here
vs.transparent = 'y'
vs.sslacceleration = 'y'
vs.checktype = 'http'
vs.checkport = "8080"
vs.checkurl = "/healthcheck.html"
vs.checkuseget = '1'
vs.checkcodes = "418"
vs.update()
