import locai
import user_tool

command_array=["user tool","loc ai"]
command_dis=["enter user tool","enter loc ai chat room"]
choses=[]
command=[]
id=[]


def home():
    print("wellcome to home page,enter help to see command")
    
def help():
    for i in range(0,len(command_array)):
        print (f"{command_array[i]}:{command_dis[i]}")

def main():
    l=0
    while True:
        if l==0:
            home()
            l=1 
        uip=input("user:")
        if uip == "home":
            home()
        elif uip == "help ":
            help()
        elif uip  == "user tool":
            user_tool()
        elif uip == "loc ai":
            locai()
        else:
            print(f"command: {uip} nofind")

main()