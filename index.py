import math
import requests
import json
from datetime import datetime
import config
import discord
import asyncio
from discord.ext import commands
import os
import embedParser

API_KEY = os.environ["API_KEY"]

NAME = os.environ["NAME"]

TAG = os.environ["TAG"]

url = f"https://api.henrikdev.xyz/valorant/v1/mmr-history/eu/{NAME}/{TAG}"

headers = {
    'Content-Type': 'application/json',
    'Authorization': API_KEY
}

# Your bot token
TOKEN = os.environ["TOKEN"]

intents = discord.Intents.default()
intents.messages = True  # Enable the messages intent
intents.message_content = True                                                                                                                                                           
started = False
embed = True
# Define the bot prefix
bot = commands.Bot(command_prefix='!', intents=intents)

# Event: Called when the bot is ready to start
@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')
    await bot.change_presence(activity=discord. Activity(type=discord.ActivityType.listening, name="Ammar's comms 🔇"))

# Command to start the loop
@bot.command(name='start')
async def start_loop(ctx):
    await ctx.send('Beginning tracking...')
    global started
    started = True
    bot.loop.create_task(begin_tracking(ctx.channel))

@bot.command(name='embed')
async def embed(ctx):
    global embed
    await ctx.send('Disabling embed' if embed else 'Enabling embed')
    embed = not embed

@bot.command(name='setUser')
async def set_user(ctx, name, tag):
    await ctx.send(f'Changing tracking to {name}#{tag}...')
    
    global NAME,TAG, url
    
    res = requests.get(f"https://api.henrikdev.xyz/valorant/v1/mmr-history/eu/{name}/{tag}", headers=headers)
    response = json.loads(res.text)
    
    if not "errors" in response:
        NAME = name
        TAG = tag
        url = f"https://api.henrikdev.xyz/valorant/v1/mmr-history/eu/{NAME}/{TAG}"
        
        await ctx.send(f'Successfully tracking {name}#{tag}')
        await stop_loop()
        await start_loop()
    else:
        await ctx.send(f'Failed to change tracking to {name}#{tag}')

async def begin_tracking(channel):
    global started 
    last_match_id = None
    while started:
        res = requests.get(url, headers=headers)

        response = json.loads(res.text)
        rr_change = response["data"][0]["mmr_change_to_last_game"]
        match_id = response["data"][0]["match_id"]

        print("Match found:", match_id )

        if match_id != last_match_id:
            url_match = f"https://api.henrikdev.xyz/valorant/v4/match/eu/{match_id}"

            res_match = requests.get(url_match, headers=headers)

            response_match = json.loads(res_match.text) 
            
            timestamp = response_match["data"]["metadata"]["started_at"]
            dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
            hr = dt.strftime("%A, %B %d, %Y %I:%M:%S %p")

            for team in response_match["data"]["teams"]:
                if team["team_id"] == "Red":
                    red_score = team["rounds"]["won"]
                else:
                    blue_score = team["rounds"]["won"]

            round_count = red_score + blue_score

            red_team = []
            blue_team = []
            for player in response_match['data']['players']:
                if player['team_id'] == 'Red':
                    red_team.append(player)
                else:
                    blue_team.append(player)
            
            outcome = "Defeat" if int(rr_change) < 0 else "Victory"

            red_team.sort(key = lambda x: x['stats']['score'], reverse=True)
            blue_team.sort(key = lambda x: x['stats']['score'], reverse=True)

            print(f"Match ID: {match_id}")
            print(f"Started at (UTC): {hr} (UTC)")
            print(f"Outcome: {outcome}")
            print(f"Red {red_score} : {blue_score} Blue")
            print(f"Map: {response_match['data']['metadata']['map']['name']}")
            print(f"RR Change: {'+' if rr_change > 0 else ''}{rr_change}")
            print("\n")
            print(f'{"Red Team":16} | {"Agent":^9} | Avg Combat Score | {"K":2} - {"D":2} - {"A":2} | {"Rank"}  \n')
            
            for player in red_team:
                print(f'{player["name"]:16} | {player["agent"]["name"]} | {math.floor(player["stats"]["score"]/round_count):^16} | {player["stats"]["kills"]:2} - {player["stats"]["deaths"]:2} - {player["stats"]["assists"]:2} | {player["tier"]["name"]}')
            print(f'\n{"Blue Team":16} | Avg Combat Score | {"K":2} - {"D":2} - {"A":2} | Rank\n')

            for player in blue_team:
                print(f'{player["name"]:16} | {player["agent"]["name"]} | {math.floor(player["stats"]["score"]/round_count):^16} | {player["stats"]["kills"]:2} - {player["stats"]["deaths"]:2} - {player["stats"]["assists"]:2} | {player["tier"]["name"]}')
            print()

            global embed
            if embed:
                outcome = 0 if int(rr_change) < 0 else 1
                
                data = { "head": {  "id" : match_id, 
                                    "timestamp" : response_match["data"]["metadata"]["started_at"],
                                    "start": hr },
                        
                        "match": { "outcome" : outcome,
                                    "rounds" : round_count, 
                                    "map" : response_match['data']['metadata']['map']['name'],
                                    "rr": rr_change},
                        
                        "teams": { "red" : { "name" : "Red", "players" : red_team, "score" : red_score },
                                    "blue" : { "name" : "Blue", "players" : blue_team, "score" : blue_score }
                        }
                    }
    
                embed_msg = embedParser.generateEmbed(data)
                if not embed_msg == None:
                    await channel.send(embed=embed_msg)
                else:
                    await channel.send('Failed to generate embed')
                    embed = False

            else:
                # Collect all the details into a single string
                output = []

                # Match details
                output.append(f"Match ID: {match_id}")
                output.append(f"Started at: {hr} (UTC)")
                output.append(f"Outcome: {outcome}")
                output.append(f"Map: {response_match['data']['metadata']['map']['name']}")
                output.append(f"RR Change: {'+' if rr_change > 0 else ''}{rr_change}")
                output.append("")
    #
                output.append(f"{f'Red {red_score} - {blue_score} Blue':^53}")
                output.append("")
                
                # Red Team stats
                output.append(f'| {"Red Team":^16} | {"Agent":^9} |  ACS  | {"K":2} - {"D":2} - {"A":2} | {"Rank":^11} |\n')
                for player in red_team:
                    output.append(f'| {player["name"]:16} | {player["agent"]["name"]:9} | {round(player["stats"]["score"]/round_count):^5} | {player["stats"]["kills"]:2} - {player["stats"]["deaths"]:2} - {player["stats"]["assists"]:2} | {player["tier"]["name"]:11} |')

                output.append("")
                # Blue Team stats
                output.append(f'\n| {"Blue Team":^16} | {"Agent":^9} |  ACS  | {"K":2} - {"D":2} - {"A":2} | {"Rank":^11} |\n')
                for player in blue_team:
                    output.append(f'| {player["name"]:16} | {player["agent"]["name"]:9} | {round(player["stats"]["score"]/round_count):^5} | {player["stats"]["kills"]:2} - {player["stats"]["deaths"]:2} - {player["stats"]["assists"]:2} | {player["tier"]["name"]:11} |')

                
                # Print the entire compiled string
                msg = "```\n" + "\n".join(output) + "\n```"
                await channel.send(msg)
        
        last_match_id = match_id

        await asyncio.sleep(30)

# Command to stop the loop
@bot.command(name='stop')
async def stop_loop(ctx):
    await ctx.send('Stopping tracking...')
    # Logic to stop the loop can be implemented here
    global started
    started = False

# @bot.command(name='last')
# async def test(ctx):
#     await ctx.send('Last game...')
    
#     res = requests.get(url, headers=headers)

#     response = json.loads(res.text)
#     rr_change = response["data"][0]["mmr_change_to_last_game"]
#     match_id = response["data"][0]["match_id"]
    
#     print("Match found:", match_id )
    
#     url_match = f"https://api.henrikdev.xyz/valorant/v4/match/eu/{match_id}"

#     res_match = requests.get(url_match, headers=headers)

#     response_match = json.loads(res_match.text) 
    
#     timestamp = response_match["data"]["metadata"]["started_at"]
#     dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
#     hr = dt.strftime("%A, %B %d, %Y %I:%M:%S %p")
    
#     for team in response_match["data"]["teams"]:
#         if team["team_id"] == "Red":
#             red_score = team["rounds"]["won"]
#         else:
#             blue_score = team["rounds"]["won"]

#     round_count = red_score + blue_score
    
#     red_team = []
#     blue_team = []
#     for player in response_match['data']['players']:
#         if player['team_id'] == 'Red':
#             red_team.append(player)
#         else:
#             blue_team.append(player)

#     outcome = 0 if int(rr_change) < 0 else 1

#     red_team.sort(key = lambda x: x['stats']['score'], reverse=True)
#     blue_team.sort(key = lambda x: x['stats']['score'], reverse=True)
    
#     data = { "head": {  "id" : match_id, 
#                         "timestamp" : response_match["data"]["metadata"]["started_at"],
#                         "start": hr },
            
#              "match": { "outcome" : outcome,
#                         "rounds" : round_count, 
#                         "map" : response_match['data']['metadata']['map']['name'],
#                         "rr": rr_change},
             
#              "teams": { "red" : { "name" : "Red", "players" : red_team, "score" : red_score },
#                         "blue" : { "name" : "Blue", "players" : blue_team, "score" : blue_score }
#              }
#     }
    
#     print(data)
    
#     embed = embedParser.generateEmbed(data)
#     if not embed == None:
#         await ctx.channel.send(embed=embed)
#     else:
#         await ctx.send('Failed')

# Run the bot with the specified token

from flask import Flask
from threading import Thread
import discord
from discord.ext import commands

app = Flask(__name__)

@app.route('/')
def health_check():
    return "OK", 200

def run_health_check_server(): 
    print("Running bogus flask server")
    app.run(host='0.0.0.0', port=8000)


t = Thread(target=run_health_check_server)
t.start()

bot.run(TOKEN)


                        
