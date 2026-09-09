import chat

if __name__ == "__main__":
  while True:
    user_input = input("請輸入你的任務: ")
    print(chat.chat_with_agent(user_input))