import json
import os


#glb_code

current_dir = os.getcwd()
setting_file = os.path.join(current_dir, 'setting.json')

with open(setting_file,'r') as file:
        setting = json.load(file)
#---
class chat:
    def url_api():
        apiurl = setting[0]["settings"]["apiurl"]
        return apiurl
    def model_name():
        model_name = setting[0]["settings"]["MODEL_NAME"]
        return model_name

class web:
    def port(port_type):
        port = setting[1]["settings"][port_type]
        print (int(port))
        return int(port)
    def ip():
        ipaddr = setting[1]["settings"]["ip"]
        print(ipaddr)
        return ipaddr



class change_setting:
    def reset_to_default():
        pass
          
        