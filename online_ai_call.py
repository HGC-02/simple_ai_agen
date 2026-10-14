import os
import json

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

def call():
    # rm priv info by loc ai --> user see the info that rm priv info by ai --> user allow or deline --> if allow send -->if deline tell why (opption)--> agian 
    pass