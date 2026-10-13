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
        

def command():
    print("id   func")
    for i in id:
        print(f"{id[i]}.:  {choses[i]}\n")
def help():
    for i in id:
        print(choses[i],",","command:",command[i])

def main():
    l=0
    while True:
        if l==0:
            command()
            l=1 
        uip=input()
        if uip == "command":
            command()
        elif uip == "help":
            help()
        else:
            print(f"command: {uip} nofind")
