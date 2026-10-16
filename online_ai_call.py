import os
import json
import setting_funtion as settings
import requests

api=""
def json_demo(name,api):
    x={
        "ai_name" : name ,
        "api" : api
    }
    return x


def init(ai_name="demo"):
    global api
    if not "pir_api.json" in os.listdir("."):
        with open("pir_api.json","w") as x:
            json.dump()
    else:
        with open("pir_aip.json","r") as x:
            v=json.load(x)
            if ai_name != "demo":
                for i in v:
                    if i["ai_name"] == ai_name:
                        api=i["api"]
            else:
                print("give a ai name")

def priv_check(user_prompt):
    # rm priv info by loc ai --> user see the info that rm priv info by ai --> user allow or deline --> if allow send -->if deline tell why (opption)--> agian 
    
    
    OLLAMA_URL = settings.chat.url_api()
    MODEL_NAME = settings.chat.model_name()
    prompt = (f"this is the user prompt:{user_prompt} \n remove the private information for user, only need to show the prompt")
    messages = [{"role": "user", "content": prompt}]
    
    payload = {
                "model": MODEL_NAME,
                "messages": messages,
                "stream": False,
            }
    response = requests.post(OLLAMA_URL, json=payload).json()
    message = response.get("message", {})
    v=True
    #=======================start loop
    while v:
        print (f"ai respone:{message}")
        x = input("is all priv info. has been remove?,y/n:")
        if x == "y":
            v = False
            break
        elif x == "Y":
            v = False
            break
        else:
            x=input("what i missing pls told me:")
            prompt = (f"this is the user prompt:{user_prompt} \n remove the private information for user, only need to show the prompt \n this is the last change by you:{message},thiss is the user suggustion:{x}")
            message = [{"role": "user", "content": prompt}]
            
            payload = {
                        "model": MODEL_NAME,
                        "messages": message,
                        "stream": False,
                    }
            response = requests.post(OLLAMA_URL, json=payload).json()
            message = response.get("message", {})
    #==============end loop start call online ai=======
    final=message
    return final

