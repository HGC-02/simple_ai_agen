import json
import subprocess
import requests
import os
import tool 
import setting_funtion as settings
from pathlib import Path

messages = []
OLLAMA_URL = settings.chat.url_api()
MODEL_NAME = settings.chat.model_name()
current_dir = Path(__file__).resolve().parent
tools_file = current_dir  / 'tools_list.json'
with open(tools_file, 'r') as file:
    tools = json.load(file)

#--- move ---
#--- rebuild ---
def payload_packer(prompt,tools_list):
  messages = [{"role": "user", "content": prompt}]

  payload = {
      "model": MODEL_NAME,
      "messages": messages,
      "tools": tools,
      "stream": False,
  }
  return payload

def call(payload):
  response = requests.post(OLLAMA_URL, json=payload).json()
  message = response.get("message", {})
  return message

def chat_with_agent(prompt,tools=tools):
  
  payload = payload_packer(prompt, tools)

  message = call(payload)

  if message.get("tool_calls"):
    messages.append(message)
    messages.extend(tool.main(message))#call tool function

    final_payload = payload_packer(prompt, tools)
    final_response = requests.post(OLLAMA_URL, json=final_payload).json()
    #print(final_payload)
    return(f"\n[Agent]: {final_response.get('message', {})}")

  else:
    return(f"\n[Agent]: {message.get('content')}")
  
