from python_kemptech_api import *

# Specify the LoadMaster connection credentials here:
loadmaster_ip = ""
username = ""
password = ""
vs_ip = ""
rs_ip_1 = ""
rs_ip_2 = ""
vs_port = ""
rs_port = ""

lm = LoadMaster(loadmaster_ip, username, password)

vs = lm.create_virtual_service(vs_ip, vs_port, "tcp")
vs.save()

# Add and save the first real server
rs1 = vs.create_real_server(rs_ip_1, rs_port)
rs1.save()

# Add and save the second real server
rs2 = vs.create_real_server(rs_ip_2, rs_port)
rs2.save()
