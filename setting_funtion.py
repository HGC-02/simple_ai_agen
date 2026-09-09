import json

#env var

#---

class chat:
    def url_api():
        with open('setting.json', 'r') as file:
            settings = json.load(file)
        apiurl = settings[0]["ai-api"]["apiurl"]
        return apiurl
    def model_name():
        with open('setting.json', 'r') as file:
            settings = json.load(file)
        model_name = settings[0]["ai-api"]["MODEL_NAME"]
        return model_name