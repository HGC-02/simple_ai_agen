import chat
import subprocess
import json

dircall = True
ai_json_file = "chat_history.json"
user_json_file = "user_input_history.json"
if __name__ == "__main__":
  while True:
    if dircall:
      user_input = input("請輸入你的任務: ")
      if user_input == "/start web":
        subprocess.Popen(["python", "main-web.py"])
        continue
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
        "inform": chat.chat_with_agent(user_input)
    }
    with open(ai_json_file, "w", encoding="utf-8") as f:
        json.dump(my_variable, f)

    # Open and parse the JSON file
    with open(ai_json_file, 'r') as file:
        data = json.load(file)

        # Extract the last/latest item in the list
        latest_var = data[-1]["inform"]
        print(latest_var)


        