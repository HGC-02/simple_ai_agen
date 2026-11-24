import json
import subprocess
import requests
import os
import sqlite3 
import setting_funtion as settings
from pathlib import Path
import init_database as init_db

current_dir = Path(__file__).resolve().parent

class get_arched_history:
  
  sql_dir= current_dir / "history" / "history.db"
  try:
    sql=sqlite3.connect(sql_dir)
  except:
    with open(sql_dir,"w") as f:
      f.close
    init_db.file_path(sql_dir)
    init_db.catalog(sql_dir)
  def get_by_tag(tag):
    self=get_arched_history
    curr=self.sql.cursor()
    ans=curr.execute("SELECT * FROM catalog WHERE tag = ?",(tag).fetchall()
    return ans
    
  def get_contex_title(id,by="id"):
    self=get_arched_history
    curr=self.sql.cursor()
    ans=curr.execute(f"SELECT title_of_history FROM summaries WHERE {by} = ?",
    (id)).fetchall
    return ans
  def get_contex(title):
    self=get_arched_history
    curr=self.sql.cursor()
    file_name=curr.execute(f"SELECT file_name FROM file_lib WHERE title_of_history = ? ",(title)).fetchall
    with open(file_name,"r") as f:
      return f
def get_current_chat_history():
  with open((current_dir/"chat_history.json","r")) as f:
    hist=f
  return hist
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



def main(tool):
    messages = []
    for tool_call in tool["tool_calls"]:
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
      return messages
