import json
import subprocess
import requests
import os

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5:7b"

# 1. tools
tools = [
        {
        "type": "function",
        "function": {
            "name": "save_to_calendar",
            "description": (
                "當用戶要求在日曆上記低行程、約會或特定日期的事件時使用。"
                "模型必須從對話中提取日期（YYYY-MM-DD 格式）與事件內容（content），"
                "並以 JSON 格式儲存。"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "事件發生的日期，格式嚴格為 YYYY-MM-DD（例如：2026-08-25）",
                    },
                    "content": {
                        "type": "string",
                        "description": "該日期的行程或事件詳細內容",
                    },
                },
                "required": ["date", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_calendar",
            "description": "當用戶詢問日曆安排、查看某日行程或所有日程時使用此工具。",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "run_bash",
            "description": "執行本地 Linux Shell 指令並返回輸出",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "要執行的 bash 指令"}
                },
                "required": ["command"],
            },
        },
    },
       {
        "type": "function",
        "function": {
            "name": "save_to_topic_note",
            "description": "當用戶要求在特定主題子目錄下記低、儲存或更新筆記時使用。模型必須從對話中提取分類主題（topic）、檔案名稱（filename）與詳細內容（content），並以 JSON 結構進行合併儲存。",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "筆記所屬的分類主題或子目錄名稱（例如：linux、python）"
                    },
                    "filename": {
                        "type": "string",
                        "description": "用作檔案名稱的簡短摘要"
                    },
                    "content": {
                        "type": "string",
                        "description": "需要記錄或合併的詳細內容"
                    }
                },
                "required": ["topic", "filename", "content"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "get_topic_notes",
            "description": "當用戶要求查看、檢索或讀取某個特定主題子目錄下的筆記時使用。模型必須從對話中提取分類主題（topic）。",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "要檢索的筆記分類主題或子目錄名稱（例如：linux、python）"
                    }
                },
                "required": ["topic"],
            },
        },
    },

]


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
    print(f"\n[Agent 回答]: {final_response.get('message', {}).get('content')}")

  else:
    print(f"\n[Agent 回答]: {message.get('content')}")


if __name__ == "__main__":
  while True:
    user_input = input("請輸入你的任務: ")
    chat_with_agent(user_input)