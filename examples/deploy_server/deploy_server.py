# Import tools
import sys
import time
import logging

from python_kemptech_api import *

# Global Parameters
_name = "deploy_server"
_debug = logging.WARNING

# Logging
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-10.10s]  %(message)s")
shortFormatter = logging.Formatter("[%(levelname)-8.8s]  %(message)s")
log = logging.getLogger()
log.setLevel(_debug)
fileHandler = logging.FileHandler("{0}/{1}.log".format("./", _name))
fileHandler.setFormatter(logFormatter)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(shortFormatter)
log.addHandler(fileHandler)
log.addHandler(consoleHandler)


# Specify the LoadMaster connection credentials here:
loadmaster_ip = ""
username = ""
password = ""
vs_ip = ""
vs_port = ""
vs_proto = ""
rs_ip = ""
rs_port = ""

lm = LoadMaster(loadmaster_ip, username, password)
vs = lm.get_virtual_service(address=vs_ip, port=vs_port, protocol=vs_proto)


def calculate_weight(vs, skip_id, percentage):
    total_weights = 0
    
    for rs_id, rs_obj in vs.servers.items():
        if rs_obj.rsindex != skip_id:
            print("RS #{}: {}".format(rs_id, rs_obj.weight))
            total_weights += int(rs_obj.weight)
            print("New weight: {}".format(total_weights))
        
    new_weight = (percentage * total_weights) / (100.0 - percentage)
    return new_weight


def main(argv):
    action = argv[0]
    
    log.info("Doing action: {}".format(action))
    
    if action == "add":
        rs_ip = argv[1]
        
        rs = vs.create_real_server(rs_ip, rs_port)
        rs.enabled = 'n'
        
        rs.save()
        
    if action == "remove":
        rs_ip = argv[1]
        
        rs = vs.get_real_server(rs_ip, rs_port)
        rs.delete()
        
    elif action == "disable":
        rs_ip = argv[1]
    
        rs = vs.get_real_server(rs_ip, rs_port)
        
        rs.enabled = 'n'
        rs.update()
    
    elif action == "drip":
        rs_ip = argv[1]
        drip_percent = int(argv[2])
    
        rs = vs.get_real_server(rs_ip, rs_port)
        
        rs.enabled = 'y'
        rs.weight = int(calculate_weight(vs, rs.rsindex, drip_percent))
        rs.update()
    
    elif action == "monitor":
        rs_ip = argv[1]
        monitor_duration = int(argv[2])
        rs = vs.get_real_server(rs_ip, rs_port)
        
        monitor_results = []
        
        for i in range(monitor_duration * 2):
            monitor_results.append(rs.status)

            if len(monitor_results) > 2 and monitor_results[-1] == "Down" and monitor_results[-2] == "Up":
                print("RS has gone down!")
            time.sleep(30)
            
        if "Down" in monitor_results:
            print("RS is unstable")
            exit(1)
        else:
            print("RS is stable")
            exit(0)
            
    elif action == "equalize":
        for rs_id, rs_obj in vs.servers.items():
            rs_obj.weight = "1000"
            rs_obj.update()


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit(0)
    except EOFError:
        sys.exit(0)
    # except:
    #     sys.exit(0)