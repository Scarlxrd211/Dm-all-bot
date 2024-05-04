import discord
import json
import time
import os
from wl import *
from colorama import *
from discord.ext import commands
from discord.ext.commands import errors

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="+", intents=intents)
bot.remove_command('help')

with open("config.json", 'r') as f:
    config = json.load(f)

@bot.event
async def on_ready():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""{Fore.LIGHTCYAN_EX}
  __   ___ __  ___ _  __   _____ __    __  __ __    __  _   _     __  __ _____  
/' _/ / _//  \| _ \ | \ \_/ / _ \ _\  | _\|  V  |  /  \| | | |   |  \/__\_   _| 
`._`.| \_| /\ | v / |_ > , <| v / v | | v | \_/ | | /\ | |_| |_  | -< \/ || |   
|___/ \__/_||_|_|_\___/_/ \_\_|_\__/  |__/|_| |_| |_||_|___|___| |__/\__/ |_|   
                   
Logged as {bot.user.name}""")

@bot.command()
async def dmall(ctx, *, message: str = None):
    guild = ctx.guild
    if message is None:
        await ctx.reply("Merci de spécifier un message à envoyer à tous les membres du serveur.")
        return
    
    for member in guild.members:
        heure_actuelle = time.localtime() 
        temps = time.strftime("[%H:%M:%S]", heure_actuelle)
        if member.id in CONFIG:
            print(f"{Fore.RED}{temps} {Fore.WHITE}Ignorer l'envoi car le membre est dans la whitelist. {member.name}")
            continue
        if member.id == bot.user.id:  
            print(f"{Fore.RED}{temps} {Fore.WHITE}Ignorer l'envoi d'un message direct au bot lui-même.")
            continue
        if member.bot:
            print(f"{Fore.RED}{temps} {Fore.WHITE}Ignorer l'envoi d'un message direct a tout les bots pour eviter les erreurs.")
            continue
        try:
            await member.send(message)
            print(f"{Fore.GREEN}{temps} {Fore.CYAN}{member.name} {Fore.WHITE}dm envoyé avec succès.")
        except discord.Forbidden:
            print(f"{Fore.RED}{temps} {Fore.WHITE}Il est impossible d'envoyer un DM à {member.name}.")
        except Exception as e:
            print(f"{Fore.RED}{temps} {Fore.WHITE}Une erreur s'est produite lors de l'envoi d'un DM à {member.name}: {e}")
        

    print(F"{Fore.RED}{temps} {Fore.WHITE}Tout les membres on été dm, heureux de vous avoir servi !")
    
@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Help",
        description=f"Pour utiliser le bot, utilisez la commande: dmall <contenu>"
    )
    await ctx.reply(embed=embed)

bot.run(config["token"])