import os
import math
import requests
import json
from datetime import datetime
import config
import discord
import asyncio
from discord.ext import commands

WIN_COL = 4289797
LOSS_COL = 13632027

COLS = [LOSS_COL,WIN_COL]

def b(a):
    return f"**{a}**"
def ita(a):
    return f"*{a}*"

ranks = {   'Iron1':1264357418150662307, 'Iron2':1264357425809588277, 'Iron3':1264357432386125976, 
            'Bronze1':1264357324995166269, 'Bronze2':1264357332184338463, 'Bronze3':1264357341025931338,
            'Silver1':1264357476900536390, 'Silver2':1264357486081871893, 'Silver3':1264357493761638471,
            'Gold1':1264357374278504570, 'Gold2':1264357382314655796, 'Gold3':1264357388857643030, 
            'Platinum1':1264357438182653972, 'Platinum2':1264357446156157019, 'Platinum3':1264357452858523660,
            'Diamond1':1264357348441325610, 'Diamond2':1264357359145324676, 'Diamond3':1264357367445717043, 
            'Ascendant1':1264357274814517359, 'Ascendant2':1264357306154356869, 'Ascendant3':1264357316140994623, 
            'Immortal1':1264357397422538752, 'Immortal2':1264357404154396713, 'Immortal3':1264357412618502155,  
            'Radiant':1264357467014303935 }

maps = { 'Sunset':'https://static.wikia.nocookie.net/valorant/images/5/5c/Loading_Screen_Sunset.png',
        'Lotus':'https://static.wikia.nocookie.net/valorant/images/d/d0/Loading_Screen_Lotus.png',
        'Pearl':'https://static.wikia.nocookie.net/valorant/images/a/af/Loading_Screen_Pearl.png',
        'Fracture':'https://static.wikia.nocookie.net/valorant/images/f/fc/Loading_Screen_Fracture.png',
        'Breeze':'https://static.wikia.nocookie.net/valorant/images/1/10/Loading_Screen_Breeze.png',
        'Icebox':'https://static.wikia.nocookie.net/valorant/images/1/13/Loading_Screen_Icebox.png',
        'Bind':'https://static.wikia.nocookie.net/valorant/images/2/23/Loading_Screen_Bind.png',
        'Haven':'https://static.wikia.nocookie.net/valorant/images/7/70/Loading_Screen_Haven.png',
        'Split':'https://static.wikia.nocookie.net/valorant/images/d/d6/Loading_Screen_Split.png',
        'Ascent':'https://static.wikia.nocookie.net/valorant/images/e/e7/Loading_Screen_Ascent.png'}

print(ranks)

def generateEmbed(data):
    embed = discord.Embed(
        title=f"Latest Match ",
        # {ita(data['head']['id'])}
        url="https://youtu.be/vdESRb6zwTE?si=WdZte0PswPYZjgAf&t=26",
        color=(COLS[data["match"]["outcome"]]))
    
    outcome_str = ("WIN" if data["match"]["outcome"] else "LOSS")
    
    embed.set_image(url=maps[data['match']['map']])
    embed.add_field(name=ita(f"Outcome {outcome_str}"),value=b(f"RRΔ {'+' if data['match']['rr'] > 0 else ''}{data['match']['rr']}"))
    # embed.add_field(name="LEADERBOARD",value="AGENT | ACS | K-D-A | RANK",inline=False)
    
    for team in data["teams"]:
        embed.add_field(name=f"――――――――――――――\n### {data['teams'][team]['name']} Team ###",value=b(" "), inline=False)
        for player in data["teams"][team]["players"]:
            print(player["name"])
            
            embed.add_field(name=f'{b(player["name"])} <:{player["tier"]["name"].replace(" ", "")}:{ranks[player["tier"]["name"].replace(" ", "")]}>',
                            value=(f'''`{player["agent"]["name"]}` {math.floor(player["stats"]["score"]/data['match']['rounds']):^16}
                                   `{player["stats"]["kills"]}-{player["stats"]["deaths"]}-{player["stats"]["assists"]}`'''))
        embed.add_field(name=' ', value=' ')
    
    embed.set_footer(text=f"{datetime.strptime(data['head']['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%d-%m-%Y %I:%M%p')} | {data['head']['id']}")
        
    return embed 