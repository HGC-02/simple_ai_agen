import json
import sys
import os

command_array=["user_tool",]
command_dis=["enter user tool"]
choses=[]
command=[]
id=[]
with open("func_list.json","r") as f:
    x=json.load(f)
    for i in x:
        choses.append(i["name"])
        command.append(i['command'])
        id.append(i["id"])
        

def home():
    print("wellcome to home page,enter help to see command")
    
def help():
    for i in len(command_array):
        print (command_array[i],command_dis[i])

def main():
    l=0
    while True:
        if l==0:
            home()
            l=1 
        uip=input()
        if uip == "home":
            home()
        elif uip == "help":
            help()
        elif uip  == "user tool":
            program = sys.executable
            arguments = [sys.executable, "user_tool_main.py"]
            os.execv(program, arguments)
            ptint("well seem like you find a erro if you would like to pls post it to issui in github thx")
        else:
            print(f"command: {uip} nofind")
