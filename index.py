import requests
import json
from datetime import datetime

import discord
import asyncio
from discord.ext import commands

API_KEY = ""

url = "https://api.henrikdev.xyz/valorant/v1/mmr-history/eu/[name]/[tag]"

headers = {
    'Content-Type': 'application/json',
    'Authorization': API_KEY
}

# Your bot token
TOKEN = ''

intents = discord.Intents.default()
intents.messages = True  # Enable the messages intent
intents.message_content = True                                                                                                                                                           
# Define the bot prefix
bot = commands.Bot(command_prefix='!', intents=intents)

# Event: Called when the bot is ready to start
@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')

# Command to start the loop
@bot.command(name='start')
async def start_loop(ctx):
    await ctx.send('Beginning tracking...')
    bot.loop.create_task(send_message_every_5_seconds(ctx.channel))

async def send_message_every_5_seconds(channel):
    last_match_id = None
    while True:
        res = requests.get(url, headers=headers)

        response = json.loads(res.text)
        rr_change = response["data"][0]["mmr_change_to_last_game"]
        match_id = response["data"][0]["match_id"]

        print("Match found:", match_id )

        if match_id != last_match_id and int(rr_change) < 0:
            url_match = f"https://api.henrikdev.xyz/valorant/v4/match/eu/{match_id}"

            res_match = requests.get(url_match, headers=headers)

            response_match = json.loads(res_match.text) 
            
            timestamp = response_match["data"]["metadata"]["started_at"]
            dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
            hr = dt.strftime("%A, %B %d, %Y %I:%M:%S %p")

            red_team = []
            blue_team = []
            for player in response_match['data']['players']:
                if player['team_id'] == 'Red':
                    red_team.append(player)
                else:
                    blue_team.append(player)

            print(f"Match ID: {match_id}")
            print(f"Started at: {hr}")
            print(f"Outcome: Loss")
            print(f"Map: {response_match['data']['metadata']['map']['name']}")
            print(f"RR Change: {rr_change}")
            print("\n")
            print(f'{"Red Team":16} {"K":2} - {"D":2} - {"A":2} | Rank\n')

            for player in red_team:
                print(f'{player["name"]:16} {player["stats"]["kills"]:2} - {player["stats"]["deaths"]:2} - {player["stats"]["assists"]:2} | {player["tier"]["name"]}')
            print(f'\n{"Blue Team":16} {"K":2} - {"D":2} - {"A":2} | Rank\n')

            for player in blue_team:
                print(f'{player["name"]:16} {player["stats"]["kills"]:2} - {player["stats"]["deaths"]:2} - {player["stats"]["assists"]:2} | {player["tier"]["name"]}')
            print()

            # Collect all the details into a single string
            output = []

            # Match details
            output.append(f"Match ID: {match_id}")
            output.append(f"Started at: {hr}")
            output.append(f"Outcome: Loss")
            output.append(f"Map: {response_match['data']['metadata']['map']['name']}")
            output.append(f"RR Change: {rr_change}")
            output.append("\n")

            # Red Team stats
            output.append(f'{"Red Team":16} {"K":2} - {"D":2} - {"A":2} | Rank\n')
            for player in red_team:
                output.append(f'{player["name"]:16} {player["stats"]["kills"]:2} - {player["stats"]["deaths"]:2} - {player["stats"]["assists"]:2} | {player["tier"]["name"]}')

            output.append("\n")
            # Blue Team stats
            output.append(f'{"Blue Team":16} {"K":2} - {"D":2} - {"A":2} | Rank\n')
            for player in blue_team:
                output.append(f'{player["name"]:16} {player["stats"]["kills"]:2} - {player["stats"]["deaths"]:2} - {player["stats"]["assists"]:2} | {player["tier"]["name"]}')


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

# Run the bot with the specified token
bot.run(TOKEN)


                        
