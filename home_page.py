import json
choses=[]
command=[]
id=[]
with open("func_list.json","r") as f:
    x=json.load(f)
    for i in x:
        choses.append(i["name"])
        command.append(i['command'])
        id.append(i["id"])
        

def list():
    print("id   func")
    for i in id:
        print(f"{id[i]}.:  {choses[i]}\n")
def help():
    for i in id:
        print(choses[i],",","command:",command[i])

def main():
    uip=input()
    if uip ==