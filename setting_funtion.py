import json

#env var

#---
#glb_code
with open('setting.json','r') as file:
            setting = json.load(file)
#---
class chat:
    def url_api():
        apiurl = setting[0]["ai-api"]["apiurl"]
        return apiurl
    def model_name():
        model_name = setting[0]["ai-api"]["MODEL_NAME"]
        return model_name

class web:
    def port(port_typre):
        port = setting[1][port_typre]
        return port
    def ip():
        ip=setting[2]["ip"]




class change_setting:
    def reset_to_default():
        pass
          
        