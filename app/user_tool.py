import init_database as init_db
import json
import os
import setting_funtion as settings
import requests
import sqlite3
from datetime import datetime,timezone
from pathlib import Path
import chat
OLLAMA_URL = settings.chat.url_api()
MODEL_NAME = settings.chat.model_name()
current_dir = Path(__file__).resolve().parent
UD = current_dir  / "UD.json"
his= current_dir / "history"
data_base=his/"history.db"
# add another tool list tool:[modifly_file]

tool=[
    {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "將指定的內容覆蓋到目標檔案中",
        "parameters": {
            "type": "object",
            "properties": {
                "file_name": {
                    "type": "string",
                    "description": "要寫入的檔案名稱或路徑"
                },
                "contex": {
                    "type": "string",
                    "description": "要寫入檔案的內容"
                }
            },
            "required": [
                "file_name",
                "contex"
            ],
        },
    },
}
]
def Add_file(file_name:str,contex):
    print(f"file name:{file_name} \n file conxet{contex} \n should i change Y/N? \n your anser:")
    x = input()
    if x == "Y" or x == "y":
      #switch to with methon(done)
      with open(file_name,"w") as f:
        f.write(contex)

    else:
       print("ok remain unchange")

class ai_sql:
    def add_sql_history(title,type,name):
        
        try:
            connect=sqlite3.connect(data_base)
        except:
            with open(data_base,"w") as f:
               f.close
            init_db.catalog(data_base)
            init_db.file_path(data_base)
            
        curr=connect.cursor()
        curr.execute("INSERT INTO file_path (title,path)VALUES(?,?)",(title,name))#add in table catalog
        curr.execute("")#add in file catlog
        connect.commit()
        connect.close()

def main():
    while True:
        user_input=input("what tool you want to run:")
        if user_input == "udf":
           UDF(current_dir / "chat_history.json")
        elif user_input == "Chat_sum":
           Chat_sum(current_dir / "chat_history.json")
        elif user_input == "/home":
           return True
        else:
           print(f"command {user_input} no found")


def UDF(chat_history):
    with open(chat_history,"r") as file:
       ch_contex = json.load(file)

    with open(UD,"r") as file:
        try:
          UD_contex = json.load(file)
          prompt = (f"not allow to run bash, no asking ,just do, base on the the chat history:{chat_history} up date the {UD} \n file{UD}'s contex:\n{UD_contex} \n file{chat_history}'s contex:\n{ch_contex}")
        except:
          UD_contex={}
          prompt = (f"not allow to run bash, no asking ,just do, base on the the chat history:{chat_history} to make a user data file in json format, file name is {UD} \n file{chat_history}'s contex:\n{ch_contex}")
    print(f"UD_contex:{UD_contex}")
    
   
    
    payload= chat.payload_packer(prompt,tool)
    print(f" \n \n payload:{payload}")
    message=chat.call(payload)
    print(f" \n \n message from agent:{message}")
    
    
    for tool_call in message["tool_calls"]:
        print(f" \n \n message from agent:{tool_call}")
        func_name = tool_call["function"]["name"]
        func_args=tool_call["function"]["arguments"]
        print(f" \n \n func_args:{func_args}")
        print(f" \n \n contex:{func_args.get('contex')}")
        Add_file(UD,str(func_args.get("contex")))
    print(f"UD file has been update with the new contex:{func_args.get('contex')}")
    return 




# add a chat summaries

def Chat_sum(chat_history):
    with open(chat_history,"r") as file:
       ch_contex = json.load(file)

    prompt = (f"base on the the chat history make a summaries and use about 10 to 250 word to explan the chat, mostly is mark the informations,use markdown format,file name use DATE_OF_FILE.md \n file{chat_history}:\n{ch_contex}")
    payload=chat.payload_packer(prompt,tool)
    
    message = chat.call(payload)
    
    print(f" \n \n message from agent full:{message}")
    for tool_call in message["tool_calls"]:
        print(f" \n \n message from agent:{tool_call}")
        func_name = tool_call["function"]["name"]
        func_args=tool_call["function"]["arguments"]
        print(f" \n \n func_args:{func_args}")
        print(f" \n \n contex:{func_args.get('contex')}")
    Add_file((his / func_args.get("file_name")),str(func_args.get("contex")))
    return



UDF(chat_history=(current_dir / "chat_history.json"))
Chat_sum(chat_history=(current_dir / "chat_history.json"))