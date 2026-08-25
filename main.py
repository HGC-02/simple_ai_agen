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
            "name": "save_to_note",
            "description": (
                "當用戶要求記低東西時使用。模型必須自行從用戶的說話中"
                "提取或總結出一個簡短的關鍵字作為檔案名稱（filename），"
                "並將詳細內容以 JSON 結構記錄下來。"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": (
                            "用作檔案名稱的簡短摘要（例如：購物清單、"
                            "linux指令筆記）"
                        ),
                    },
                    "content": {
                        "type": "string",
                        "description": "需要記錄的詳細內容",
                    },
                },
                "required": ["filename", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_notes",
            "description": "當用戶詢問之前記了什麼、查看記事簿、或者需要檢索歷史筆記時使用此工具。",
            "parameters": {
                "type": "object",
                "properties": {},  # 不需要額外參數，直接讀取全部
            },
        },
    },
]


# function of tools
def get_notes():
  # 改為對應當前專案資料夾下的 ai_notes
  notes_dir = os.path.join(os.path.dirname(__file__), "ai_notes")
  if not os.path.exists(notes_dir):
    return "目前沒有任何記事簿檔案。"

  files = os.listdir(notes_dir)
  if not files:
    return "記事簿目錄是空的。"

  all_notes = []
  for file in files:
    if file.endswith(".json"):
      file_path = os.path.join(notes_dir, file)
      try:
        with open(file_path, "r", encoding="utf-8") as f:
          all_notes.append(json.load(f))
      except Exception:
        continue

  return json.dumps(all_notes, ensure_ascii=False, indent=2)


def save_to_note(filename, content):
  # 改為對應當前專案資料夾下的 ai_notes
  notes_dir = os.path.join(os.path.dirname(__file__), "ai_notes")
  os.makedirs(notes_dir, exist_ok=True)

  # 清理檔名中的非法字元（避免路徑問題）
  safe_filename = "".join(
      c for c in filename if c.isalnum() or c in (" ", "-", "_")
  ).strip()
  if not safe_filename:
    safe_filename = "unnamed_note"

  file_path = os.path.join(notes_dir, f"{safe_filename}.json")

  # 組織成 JSON 格式的資料結構
  note_data = {"filename": safe_filename, "content": content}

  # 寫入獨立的 JSON 檔案
  with open(file_path, "w", encoding="utf-8") as f:
    json.dump(note_data, f, ensure_ascii=False, indent=2)

  return f"成功建立筆記檔案：{safe_filename}.json，內容已 JSON 格式儲存。"

def run_bash(command):
  try:
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True, timeout=30
    )
    return result.stdout if result.returncode == 0 else result.stderr
  except Exception as e:
    return str(e)
def save_to_calendar(date, content):
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

  # 檢查模型是否要求調用工具
  if message.get("tool_calls"):
    messages.append(message)

    for tool_call in message["tool_calls"]:
      func_name = tool_call["function"]["name"]
      func_args = tool_call["function"]["arguments"]

      if isinstance(func_args, str):
        func_args = json.loads(func_args)

      output = ""
      if func_name == "run_bash":
        output = run_bash(func_args.get("command", ""))
      elif func_name == "save_to_note":
        # 修正：將原本的 title 改為 filename，對應 tools 定義
        output = save_to_note(
            func_args.get("filename"), func_args.get("content")
        )
      elif func_name == "get_notes":
        output = get_notes()
      elif func_name == "save_to_calendar":
        output = save_to_calendar(
            func_args.get("date"), func_args.get("content")
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
