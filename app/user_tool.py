import init_database as init_db
import json
import os
import setting_funtion as settings
import requests
import sqlite3
from datetime import datetime,timezone
from pathlib import Path
import chat
import time

tool = [
    {
    "type": "function",
    "function": {
        "name": "udre-write",
        "description": "rewrite the ud",
        "parameters": {
            "type": "object",
            "properties": {
                
                "contex": {
                    "type": "string",
                    "description": "the file contex, the content will be write in to the file and it in markdown format",
                }
            },
            "required": [
                "name",
                "contex"
            ],
        },
    },
}
]
chatsumtool=[
    {
    "type": "function",
    "function": {
        "name": "add_history",
        "description": "add a file with the content to the system and will in put in to a catalog and file_path table in the database",
        "parameters": {
            "type": "object",
            "properties": {
                "tag": {
                    "type": "string",
                    "description": "a tag for file",
                },
                "contex": {
                    "type": "string",
                    "description": "the file contex, the content will be write in to the file",
                },
                "title": {
                    "type": "string",
                    "description": "the title of the file,simple and easy to understand by both human and ai and only allow VARCHAR(225)",
                },
            },
            "required": [
                "tag",
                "contex",
                "title"
            ],
        },
    },
}
]

OLLAMA_URL = settings.chat.url_api()
MODEL_NAME = settings.chat.model_name()
current_dir = Path(__file__).resolve().parent
UD = current_dir  / "UD.md"
his= current_dir / "history"
data_base=his/"history.db"


def UID():
    return str(time.time()%7*time.time()%2024)
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
    
    def add_sql_history(title,type_name,name):
        
        try:
            connect=sqlite3.connect(data_base)
        except:
            with open(data_base,"w") as f:
               f.close
            init_db.catalog(data_base)
            init_db.file_path(data_base)
            
        curr=connect.cursor()
        curr.execute("CREATE TABLE IF NOT EXISTS catalog (id INTEGER PRIMARY KEY,time VARCHAR(13),title VARCHAR(225),tag);")
        connect.commit()
        curr.execute("CREATE TABLE IF NOT EXISTS file_path (id INTEGER PRIMARY KEY,title VARCHAR(255),path)")#name file path (id PK ,title FK ,path(path return to ai))
        connect.commit()
        curr.execute("INSERT INTO catalog (title,tag)VALUES(?,?)",(title,type_name))#add in sql catlog
        connect.commit()
        curr.execute("INSERT INTO file_path (title,path)VALUES(?,?)",(title,name))#add in file_path
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
          prompt = (f"not allow to run bash,must use tool, no asking ,just do, base on the the chat history:{chat_history} to make a user data file in json format, file name is {UD} \n file{chat_history}'s contex:\n{ch_contex}")
    print(f"UD_contex:{UD_contex}")
    
   
    
    payload= chat.payload_packer(prompt,tool,sysprompt="you are a ai agent, You must call the add_history tool.you are not allowed to reply with normal text or just in 3 word.")
    print(f" \n \n payload:{payload}")
    message=chat.call(payload)
    print(f" \n \n message from agent:{message}")
    
    
    for tool_call in message["tool_calls"]:
        print(f" \n \n message from agent:{tool_call}")
        func_name = tool_call["function"]["name"]
        func_args=tool_call["function"]["arguments"]
        Add_file(UD,str(func_args.get("contex")))
    
    return 




# add a chat summaries

def Chat_sum(chat_history):
    name = (his/f"{UID()}.md")
    with open(chat_history,"r") as file:
       ch_contex = json.load(file)

    prompt = (f"base on the the chat history:{chat_history} to make a summaries and put it into Markdown format and only need the summaries \n file{chat_history}:\n{ch_contex}")
    payload=chat.payload_packer(prompt)
    message = chat.call(payload)
    contex = message.get("content")

    prompt = (f"base on the the chat history:{chat_history} to make a tag for the summaries and only need the tag \n file{chat_history}:\n{ch_contex}\n summaries:\n{contex}")
    payload=chat.payload_packer(prompt)
    message = chat.call(payload)
    tag = message.get("content")

    prompt = (f"base on the the chat history:{chat_history} to make a title for the summaries and only need the title \n file{chat_history}:\n{ch_contex}\n summaries:\n{contex}\n tag:\n{tag}")
    payload=chat.payload_packer(prompt)
    message = chat.call(payload)
    title = message.get("content")

    ai_sql.add_sql_history(title=title,type_name=tag,name=str(name))
    Add_file(str(name),contex)
#by 3 way push 1.make contex 2.make a tag for them 3.add both contex and tag into a sql database with a file path to the contex file


#UDF(chat_history=(current_dir / "chat_history.json"))
Chat_sum(chat_history=(current_dir / "chat_history.json"))