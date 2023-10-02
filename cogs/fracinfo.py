import requests
import discord
from discord import app_commands
from discord.ext import commands

orgs = [
  {
    "id": 1,
    "name": "LS_Police"
  },
  {
    "id": 2,
    "name": "RCSD"
  },
  {
    "id": 3,
    "name": "FBI"
  },
  {
    "id": 4,
    "name": "SF_Police"
  },
  {
    "id": 5,
    "name": "LS_Hospital"
  },
  {
    "id": 6,
    "name": "LS_Government"
  },
  {
    "id": 7,
    "name": "LV_Maximum_Security_Prison"
  },
  {
    "id": 8,
    "name": "SF_Hospital"
  },
  {
    "id": 9,
    "name": "Licensing_Center"
  },
  {
    "id": 10,
    "name": "TV_Studio"
  },
  {
    "id": 11,
    "name": "Grove_Street"
  },
  {
    "id": 12,
    "name": "Los_Santos_Vagos"
  },
  {
    "id": 13,
    "name": "East_Side_Ballas"
  },
  {
    "id": 14,
    "name": "Varrios_Los_Aztecas"
  },
  {
    "id": 15,
    "name": "The_Rifa"
  },
  {
    "id": 16,
    "name": "Russian_Mafia"
  },
  {
    "id": 17,
    "name": "Yakuza"
  },
  {
    "id": 18,
    "name": "La_Cosa_Nostra"
  },
  {
    "id": 19,
    "name": "Warlock_MC"
  },
  {
    "id": 20,
    "name": "LS_Army"
  },
  {
    "id": 21,
    "name": "Central_Bank"
  },
  {
    "id": 22,
    "name": "LV_Hospital"
  },
  {
    "id": 23,
    "name": "LVPD"
  },
  {
    "id": 24,
    "name": "LV_TV_Studio"
  }
]

frac_list = []
for frac in orgs:
    name = frac['name']
    frac_list.append(discord.app_commands.Choice(name=str(name).lower(), value=frac['id']))

def send_frac_info(serverid, fracid):
    members = []
    frac = requests.get(f"https://backend.arizona-rp.com/fraction/get-players?serverId={serverid}&fractionId={fracid}", headers={'Referer': 'https://arizona-rp.com/'})
    member_info = frac.json()['items']
    i = 0
    orgname = orgs[fracid-1]['name']
    embed = discord.Embed(title=f'Фракция {orgname}')
    for member in member_info:
        i += 1
        if member['isLeader']:
            embed.add_field(name="Лидер", value=f"Ник: {member['name']} ({member['rankLabel']})", inline=False)
        else:
            if member['rank'] >= 7:
                member_data = {'nick': member['name'], 'rank': member['rank'],'rankname': member['rankLabel']}
                test = f"Ник: {member['name']} | Ранг: {member['rankLabel']}({member['rank']})"
                members.append(test)
    members_str = "\n".join(members)
    embed.add_field(name="Сотрудники", value=members_str, inline=False)
    embed.add_field(name="Всего сотрудников во фракции", value=str(i) + " Человек")
    return embed


class get_frac_command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("[SYSTEM]: Команда получения информации о фракциях запущена")

    @app_commands.command(name='getorginfo', description="Получение информации о фракциях")
    @app_commands.describe(frac="Выберите фракцию", serverid="Выберите номер сервера")
    @app_commands.choices(frac=frac_list)
    async def send(self, interaction: discord.Interaction, frac: discord.app_commands.Choice[int], serverid: int):
        if serverid == 101 or serverid == 102 or serverid == 103:
            await interaction.response.send_message(embed=send_frac_info(serverid, frac.value))
            return
        if serverid > 26 or serverid < 1:
            await interaction.response.send_message("Введите id сервера от 1 до 26, или мобайл 101, 102 или 103")
            return
        await interaction.response.send_message(embed=send_frac_info(serverid, frac.value))
        

async def setup(bot):
    await bot.add_cog(get_frac_command(bot))