import json

#env var

#---
#glb_code
with open('setting.json','r') as file:
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
        return port
    def ip():
        ipaddr = setting[1]["settings"]["ip"]
        return ipaddr



class change_setting:
    def reset_to_default():
        pass
          
        