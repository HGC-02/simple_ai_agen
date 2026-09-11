import json
import subprocess
import requests
import os
import setting_funtion as settings

OLLAMA_URL = settings.chat.url_api()
MODEL_NAME = settings.chat.model_name()

with open('tools_list.json', 'r') as file:
    tools = json.load(file)



# function of tools
def save_to_topic_note(topic, filename, content):
  # 防禦性檢查：若 topic 或 filename 丟失或為 None 賦予預設值
  if not topic:
    topic = "general"
  if not filename:
    filename = "unnamed_note"

  # 1. 建立在 ai_notes 底下的子目錄
  base_dir = os.path.join(os.path.dirname(__file__), "ai_notes")
  topic_dir = os.path.join(base_dir, topic)
  os.makedirs(topic_dir, exist_ok=True)

  # 2. 清理檔名
  safe_filename = "".join(
      c for c in filename if c.isalnum() or c in (" ", "-", "_")
  ).strip()
  if not safe_filename:
    safe_filename = "unnamed_note"

  file_path = os.path.join(topic_dir, f"{safe_filename}.json")

  # 3. 讀取現有內容並進行合併
  existing_data = []
  if os.path.exists(file_path):
    try:
      with open(file_path, "r", encoding="utf-8") as f:
        loaded = json.load(f)
        if isinstance(loaded, list):
          existing_data = loaded
        else:
          existing_data = [loaded]
    except Exception:
      existing_data = []

  # 新增本次內容
  new_entry = {"content": content}
  existing_data.append(new_entry)

  # 4. 寫回合併後的 JSON
  with open(file_path, "w", encoding="utf-8") as f:
    json.dump(existing_data, f, ensure_ascii=False, indent=2)

  return (
      f"成功在主題【{topic}】下更新筆記檔案：{safe_filename}.json，已完成內容合併。"
  )

def get_topic_notes(topic):
  if not topic:
    return "未指定要檢索的主題名稱。"
    
  base_dir = os.path.join(os.path.dirname(__file__), "ai_notes")
  topic_dir = os.path.join(base_dir, topic)
  
  if not os.path.exists(topic_dir):
    return f"找不到主題【{topic}】的分類目錄。"

  files = os.listdir(topic_dir)
  if not files:
    return f"主題【{topic}】的目錄是空的。"

  all_topic_notes = []
  for file in files:
    if file.endswith(".json"):
      file_path = os.path.join(topic_dir, file)
      try:
        with open(file_path, "r", encoding="utf-8") as f:
          all_topic_notes.append(json.load(f))
      except Exception:
        continue

  return json.dumps(all_topic_notes, ensure_ascii=False, indent=2)

def run_bash(command):
  try:
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True, timeout=30
    )
    return result.stdout if result.returncode == 0 else result.stderr
  except Exception as e:
    return str(e)

def save_to_calendar(date, content):
  if not date:
    date = "unnamed_date"
    
  cal_dir = os.path.join(os.path.dirname(__file__), "ai_calendar")
  os.makedirs(cal_dir, exist_ok=True)

  safe_date = "".join(
      c for c in date if c.isalnum() or c in ("-", "_")
  ).strip()
  if not safe_date:
    safe_date = "unnamed_date"

  file_path = os.path.join(cal_dir, f"{safe_date}.json")
  cal_data = {"date": safe_date, "content": content}

  with open(file_path, "w", encoding="utf-8") as f:
    json.dump(cal_data, f, ensure_ascii=False, indent=2)

  return f"成功在日曆中記錄：{safe_date}.json，內容已 JSON 格式儲存。"


def get_calendar():
  cal_dir = os.path.join(os.path.dirname(__file__), "ai_calendar")
  if not os.path.exists(cal_dir):
    return "目前沒有任何日曆行程檔案。"

  files = os.listdir(cal_dir)
  if not files:
    return "日曆目錄是空的。"

  all_events = []
  for file in files:
    if file.endswith(".json"):
      file_path = os.path.join(cal_dir, file)
      try:
        with open(file_path, "r", encoding="utf-8") as f:
          all_events.append(json.load(f))
      except Exception:
        continue

  return json.dumps(all_events, ensure_ascii=False, indent=2)


# 2. 與 Ollama 互動的主迴圈
def chat_with_agent(prompt):
  messages = [{"role": "user", "content": prompt}]

  payload = {
      "model": MODEL_NAME,
      "messages": messages,
      "tools": tools,
      "stream": False,
  }

  response = requests.post(OLLAMA_URL, json=payload).json()
  message = response.get("message", {})

  if message.get("tool_calls"):
    messages.append(message)

    for tool_call in message["tool_calls"]:
      func_name = tool_call["function"]["name"]
      func_args = tool_call["function"]["arguments"]

      if isinstance(func_args, str):
        try:
          func_args = json.loads(func_args)
        except Exception:
          func_args = {}

      output = ""
      if func_name == "run_bash":
        output = run_bash(func_args.get("command", ""))
      elif func_name == "save_to_topic_note":
        output = save_to_topic_note(
            func_args.get("topic"), 
            func_args.get("filename"), 
            func_args.get("content")
        )
      elif func_name == "get_topic_notes":
        output = get_topic_notes(func_args.get("topic"))
      elif func_name == "save_to_calendar":
        output = save_to_calendar(
            func_args.get("date"), 
            func_args.get("content")
        )
      elif func_name == "get_calendar":
        output = get_calendar()

      messages.append(
          {
              "role": "tool",
              "content": str(output),
          }
      )

    final_payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False,
    }
    final_response = requests.post(OLLAMA_URL, json=final_payload).json()
    return(f"\n[Agent 回答]: {final_response.get('message', {}).get('content')}")

  else:
    return(f"\n[Agent 回答]: {message.get('content')}")
