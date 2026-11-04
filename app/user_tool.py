import json
import os
import setting_funtion as settings
import requests

OLLAMA_URL = settings.chat.url_api()
MODEL_NAME = settings.chat.model_name()
UD = "UD.json"
# add another tool list tool:[modifly_file]

tool={
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "將指定的內容寫入或覆蓋到目標檔案中",
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
def main():
    while True:
        user_input=input("what tool you want to run:")
        if user_input == "udf":
           UDF("chat_history.json")
        elif user_input == "Chat_sum":
           Chat_sum("chat_history.json")
        elif user_input == "/home":
           return True
        else:
           print(f"command {user_input} no found")


def UDF(chat_history):
    with open(UD,"r") as file:
        try:
          UD_contex = json.load(file)
        except:
          UD_contex="new user no data about him/her"
          
    with open(chat_history,"r") as file:
       ch_contex = json.load(file)

    prompt = (f"base on the the chat history:{chat_history} up date the {UD}")
    messages = [{"role": "user", "content": prompt}]
    
    
    messages.append(
              {
                  "role": "user",
                  "content": f"file{UD}:\n{UD_contex} \n file{chat_history}:\n{ch_contex}",
              }
          )
    
    payload = {
              "model": MODEL_NAME,
              "messages": messages,
              "tools": tool,
              "stream": False,
          }
    response = requests.post(OLLAMA_URL, json=payload).json
    while True:
        message = response.get("message", {})
        print(message)
        temp =+1
        if message != {} or temp<=10:
           break

    if message.get("tool_calls"):
        messages.append(message)
    
        for tool_call in message["tool_calls"]:
          #func_name = tool_call["function"]["name"]
          func_args = tool_call["function"]["arguments"]

          output=[
             func_args.get("file_name"),
             func_args.get("contex")
            ]
        messages.append(
                {
                    "role": "tool",
                    "content": str(output),
                }
            )


def file(file_name:str,contex):
    print(f"file name:{file_name} \n file conxet{contex} \n are you should i change Y/N? \n your anser:")
    x = input()
    if x == "Y" or x == "y":
      fd = os.open(file_name, os.O_WRONLY | os.O_CREAT)
      byte_data = contex.encode("utf-8")
      bytes_written = os.write(fd, byte_data)

    else:
       print("ok remain unchange")



# add a chat summaries

def Chat_sum(chat_history):
    with open(chat_history,"r") as file:
       ch_contex = json.load(file)

    prompt = (f"base on the the chat history:{chat_history} make a summaries and use about 10 to 250 word to explan the chat, mostly is mark the informations \n")
    messages = [{"role": "user", "content": prompt}]
    
    
    messages.append(
              {
                  "role": "user",
                  "content": f"file{chat_history}:\n{ch_contex}",
              }
          )
    
    payload = {
              "model": MODEL_NAME,
              "messages": messages,
              "tools": tool,
              "stream": False,
          }
    response = requests.post(OLLAMA_URL, json=payload).json()
    message = response.get("message", {})

    if message.get("tool_calls"):
        messages.append(message)
    
        for tool_call in message["tool_calls"]:
          func_name = tool_call["function"]["name"]
          func_args = tool_call["function"]["arguments"]

          output=[
             func_args.get("file_name"),
             func_args.get("contex")
          ]
    messages.append(
              {
                  "role": "tool",
                  "content": str(output),
              }
          )