import json
import os
import setting_funtion as settings
import requests

OLLAMA_URL = settings.chat.url_api()
MODEL_NAME = settings.chat.model_name()
UD = "UD.json"

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
              "stream": False,
          }
    response = requests.post(OLLAMA_URL, json=payload).json()
    message = response.get("message", {})