import math
from datetime import datetime
import discord

WIN_COL = 4289797
LOSS_COL = 13632027

COLS = [LOSS_COL,WIN_COL]

def b(a):
    return f"**{a}**"
def ita(a):
    return f"*{a}*"

ranks = {   'Iron1':1264549482985558088, 'Iron2':1264549499263516692, 'Iron3':1264549509107552316, 
            'Bronze1':1264549523188092938, 'Bronze2':1264549533682237555, 'Bronze3':1264549543236735076,
            'Silver1':1264549558583558237, 'Silver2':1264549575205847161, 'Silver3':1264549586333204561,
            'Gold1':1264549620369850368, 'Gold2':1264549633158418504, 'Gold3':1264549643375612016, 
            'Platinum1':1264549655036039241, 'Platinum2':1264549665429258314, 'Platinum3':1264549676028399677,
            'Diamond1':1264549711839232031, 'Diamond2':1264549732379004950, 'Diamond3':1264549748329807872, 
            'Ascendant1':1264549759017029743, 'Ascendant2':1264549768433107045, 'Ascendant3':1264549778084073514, 
            'Immortal1':1264549813173616700, 'Immortal2':1264549825878163517, 'Immortal3':1264549838956003412,  
            'Radiant':1264549852940075078, 'Unrated':1264599232631799852 }

maps = { 'Sunset':'https://static.wikia.nocookie.net/valorant/images/5/5c/Loading_Screen_Sunset.png',
        'Lotus':'https://static.wikia.nocookie.net/valorant/images/d/d0/Loading_Screen_Lotus.png',
        'Pearl':'https://static.wikia.nocookie.net/valorant/images/a/af/Loading_Screen_Pearl.png',
        'Fracture':'https://static.wikia.nocookie.net/valorant/images/f/fc/Loading_Screen_Fracture.png',
        'Breeze':'https://static.wikia.nocookie.net/valorant/images/1/10/Loading_Screen_Breeze.png',
        'Icebox':'https://static.wikia.nocookie.net/valorant/images/1/13/Loading_Screen_Icebox.png',
        'Bind':'https://static.wikia.nocookie.net/valorant/images/2/23/Loading_Screen_Bind.png',
        'Haven':'https://static.wikia.nocookie.net/valorant/images/7/70/Loading_Screen_Haven.png',
        'Split':'https://static.wikia.nocookie.net/valorant/images/d/d6/Loading_Screen_Split.png',
        'Ascent':'https://static.wikia.nocookie.net/valorant/images/e/e7/Loading_Screen_Ascent.png',
        'Abyss':'https://www.vpesports.com/wp-content/uploads/2024/06/Screenshot_4-19.png'}

mapDefault = ""

print(ranks)

def generateEmbed(data):
    embed = discord.Embed(
        title=f"Latest Match ",
        # {ita(data['head']['id'])}
        url="https://youtu.be/vdESRb6zwTE?si=WdZte0PswPYZjgAf&t=26",
        color=(COLS[data["match"]["outcome"]]))
    
    outcome_str = ("WIN" if data["match"]["outcome"] else "LOSS")
    
    mapImage = maps.get(data['match']['map'], mapDefault)
    print(f'Map is invalid? {mapImage == mapDefault}' )
    
    embed.set_image(url=mapImage)
    embed.add_field(name=ita(f"Outcome {outcome_str}"),value=b(f"RRΔ {'+' if data['match']['rr'] > 0 else ''}{data['match']['rr']}"))
    # embed.add_field(name="LEADERBOARD",value="AGENT | ACS | K-D-A | RANK",inline=False)
    
    for team in data["teams"]:
        embed.add_field(name=f"――――――――――――――――――――――――――――\n### {data['teams'][team]['name']} Team ###",value=b(" "), inline=False)
        for player in data["teams"][team]["players"]:
            print(player["name"])
            
            rankIcon = ranks.get(player["tier"]["name"].replace(" ", ""), '')
            rankIcon = f'<:{rankIcon}:{ranks[player["tier"]["name"].replace(" ", "")]}>' if not rankIcon == '' else ''
            
            print(f'Emblem is invalid? {rankIcon == ""}' )
            
            embed.add_field(name=f'{b(player["name"])} {rankIcon}',
                            value=(f'''`{player["agent"]["name"]}` 
                                   `{player["stats"]["kills"]}-{player["stats"]["deaths"]}-{player["stats"]["assists"]}` {math.floor(player["stats"]["score"]/data['match']['rounds']):^16}'''))
        embed.add_field(name=' ', value=' ')
    
    embed.set_footer(text=f"{datetime.strptime(data['head']['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%d-%m-%Y %I:%M%p')} | {data['head']['id']}")
        
    return embed 