import chat
import subprocess
import json
import os
import sys

dircall = True
ai_json_file = "chat_history.json"
user_json_file = "user_input_history.json"
if __name__ == "__main__":
  while True:
    if dircall:
      user_input = input("請輸入你的任務: ")
      ans=chat.chat_with_agent(user_input)
      print(ans)
      
      if user_input == "/start web":
        subprocess.Popen(["python", "main-web.py"])
        continue
      elif user_input == "/home":
        program = sys.executable
        arguments = [sys.executable, "home.py"]
        os.execv(program, arguments)
        ptint("well seem like you find a erro if you would like to pls post it to issui in github thx")
      
    else:
      with open(user_json_file, 'r') as file:
              data = json.load(file)
      
              # Extract the last/latest item in the list
              latest_var = data[-1]["received_data"]
              user_input=latest_var
    #---------input end--------------

    my_variable = {
        "type": "ai respon",
        "user": user_input,
        "inform": ans
    },

    

    try:
      with open(ai_json_file, "r", encoding="utf-8") as file:
          data = json.load(file)
    except FileNotFoundError:
    # If the file doesn't exist yet, start with an empty list
      data = []

# 3. Append the new item to your list
    data.append(my_variable)

# 4. Overwrite the file with the updated data
    with open(ai_json_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    with open(ai_json_file,"r") as f:
      data=json.load(f)


        