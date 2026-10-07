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

def UDF(chat_history):
    with open(UD,"r") as file:
       UD_contex = json.load(file)
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
    response = requests.post(OLLAMA_URL, json=payload).json()
    message = response.get("message", {})

    if message.get("tool_calls"):
        messages.append(message)
    
        for tool_call in message["tool_calls"]:
          func_name = tool_call["function"]["name"]
          func_args = tool_call["function"]["arguments"]

          output=file(
             func_args.get("file_name"),
             func_args.get("contex")
          )
    messages.append(
              {
                  "role": "tool",
                  "content": str(output),
              }
          )


def file(file_name,contex):
    print(f"file name:{file_name} \n file conxet{contex} \n are you should i change Y/N? \n your anser:")
    x = input()
    if x == "Y" or x == "y":
       with os.open(file_name, "w") as f:
        f.write(contex)
    else:
       print("ok remain unchange")