import sys
import time
from python_kemptech_api import *

wait_time = 10
max_retries = 10

# Specify the LoadMaster connection credentials here:
loadmaster_ip = ""
username = ""
password = ""
# Specify the Virtual Service and Real Server IDs here:
virtual_service_id = 0
real_server_id = 0

lm = LoadMaster(loadmaster_ip, username, password)
vs = lm.vs[virtual_service_id]
rs = vs.servers[real_server_id]

def get_rs_stats():
    stats = lm.stats()['Response']['Success']['Data']
    rs_stats = stats['Rs']
    if not isinstance(rs_stats, list):
        rs_stats = [rs_stats]
    rs_stats = [rs for rs in rs_stats if rs['RSIndex'] == str(real_server_id)]

    if not len(rs_stats) == 1:
        print("Could not find the RS stats by index {}".format(real_server_id))
    
    rs_stats = rs_stats[0]
    return rs_stats

# Get the drain time
drain_time = lm['finalpersist']
print("Getting initial finalpersist value: {}".format(drain_time))

# Check if dropatdrainend value and enable it
initial_drop_at_end = lm['dropatdrainend']
print("Getting initial dropatdrainend value: {}".format(initial_drop_at_end))
print("Setting dropatdrainend to Yes")
lm['dropatdrainend'] = 'Y'

# Disable the RS
print("Disabling the RS")
rs.enable = "N"
rs.update()

# Wait the specified amount
print("Waiting {} seconds for the drain timer to end".format(drain_time))
time.sleep(int(drain_time))

# Verify no active connections
rs_stats = get_rs_stats()

retries = 0
while (int(rs_stats['ActivConns']) > 0 or int(rs_stats['ConnsPerSec']) > 0) and retries <= max_retries:
    print("Real Server still has connections attached, waiting {} seconds".format(wait_time))
    time.sleep(wait_time)
    retries += 1
    rs_stats = get_rs_stats()

if retries > max_retries:
    print("Real Server still had active connections after delay")
    sys.exit(1)

# Reset initial_drop_at_end to initial value
print("Resetting dropatdrainend to initial value")
lm['dropatdrainend'] = initial_drop_at_end

print("RS #{} on VS #{} has been successfully disabled and drained".format(virtual_service_id, real_server_id))
