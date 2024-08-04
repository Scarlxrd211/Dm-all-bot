import os
import sys
import time
import json
import discord
from colorama import *
from wl import WHITELIST
from datetime import datetime
from discord.ext import commands

R = Fore.RED
B = Fore.BLUE
W = Fore.WHITE
G = Fore.GREEN
Y = Fore.YELLOW

with open('config.json', 'r') as f:
    config = json.load(f)

def clear():
    os.system("cls")

def banner():
    return """
██████╗ ██╗███████╗ ██████╗ ██████╗ ██████╗ ██████╗     ██████╗ ███╗   ███╗     █████╗ ██╗     ██╗     
██╔══██╗██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗    ██╔══██╗████╗ ████║    ██╔══██╗██║     ██║     
██║  ██║██║███████╗██║     ██║   ██║██████╔╝██║  ██║    ██║  ██║██╔████╔██║    ███████║██║     ██║     
██║  ██║██║╚════██║██║     ██║   ██║██╔══██╗██║  ██║    ██║  ██║██║╚██╔╝██║    ██╔══██║██║     ██║     
██████╔╝██║███████║╚██████╗╚██████╔╝██║  ██║██████╔╝    ██████╔╝██║ ╚═╝ ██║    ██║  ██║███████╗███████╗
╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝     ╚═════╝ ╚═╝     ╚═╝    ╚═╝  ╚═╝╚══════╝╚══════╝    
                                                                                       by scarlxrd_1337
                                                      Github: https://github.com/Scarlxrd211/dm-all-bot
"""

def panel(name, bot_id, status, guild_id, gm_count, gname, wl):
    print(f"""
{B}[@] Bot Name: {W}{name}
{B}[@] Bot ID: {W}{bot_id}
{B}[@] Status: {W}{status}
{B}[@] Guild Name: {W}{gname}
{B}[@] Guild ID: {W}{guild_id}
{B}[@] Member In Guild: {W}{gm_count}
{B}[@] Whitelist Enabled: {W}{wl}""")
    return

async def send_message(guild_id, bot, message, member, whitelist):
    guild = bot.get_guild(int(guild_id))
    message = message.replace("|", "\n")

    if guild:
        try:
            if whitelist == "Enabled":
                if member.id in WHITELIST:
                    print(f'{W}{dnow()}{Y}[!] Member {W}{member.name}{Y} Skipped (is in whitelist).')
                    pass
                else:
                    now = time.time()
                    await member.send(message)
                    print(f'{W}{dnow()}{G}[+] Member {W}{member.name}{G} Message Sent Successfuly. {W}Time Taken: {time.time() - now:.2f} sec') 
            else:
                now = time.time()
                await member.send(message)
                print(f'{W}{dnow()}{G}[+] Member {W}{member.name}{G} Message Sent Successfuly. {W}Time Taken: {time.time() - now:.2f} sec') 
        except Exception as e:
            print(f'{W}{dnow()}{R}[!] Failed To Message Member: {W}{member.name}{R}')
    else:
        print(f'{R}[X] Guild Not Found !')
        time.sleep(2)
        sys.exit(2)


def dnow():
    return f"[{datetime.now().strftime('%H:%M:%S')}]"

bot = commands.Bot(command_prefix="+", intents=discord.Intents.all())

@bot.event
async def on_ready():
    clear()
    count = 0
    server_id = int(input(f'{B}[?] Enter Server ID: '))
    message = str(input(rf'{B}[?] Message You Want To Sent (| for line feed): '))
    whitelist = str(input(f'{B}[?] Do You Want Enable Whitelist ?: '))
    wl = ""
    if whitelist.lower() == 'yes' or whitelist.lower() == 'y':
        wl += "Enabled"
    else:
        wl += "Disabled"
        
    guild = bot.get_guild(server_id)
    if guild:
        await bot.change_presence(activity=discord.Game(name=config['status'] if config['status'] != "" else "discord.gg/sakuza"))
        status =  config['status'] if config["status"] != "" else "Status not set"
        clear()
        print(banner())
        panel(bot.user.name, bot.user.id, status, guild.id, guild.member_count, guild.name, wl)        
        input(f"{B}[+] Press Enter To Start Dm All...")
        clear()
        for member in guild.members:
            await send_message(guild.id, bot, message, member, wl)
            count += 1
        print(f"{B}[!] {count} Messages Sent. Thank You For Using.")
        input(f"{B}[+] Press Enter To exit...")
        sys.exit(2)


bot.run(config['token'])