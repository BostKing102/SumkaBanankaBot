import discord
from discord import app_commands
from discord.ext import commands
import json

with open('bd/speakersMO.json', 'r') as f:
    recons_mo = json.load(f)

class GEIregister(discord.ui.Modal):
    cockie = discord.ui.TextInput(label="Куки файлы")
    user_agent = discord.ui.TextInput(label="Юзер Агент")
    def __init__(self) -> None:
        super().__init__(title="Регистрация", timeout=None)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        recons_mo[str(interaction.user.id)]['cockie'] = str(self.cockie)
        recons_mo[str(interaction.user.id)]['user_agent'] = str(self.user_agent)
        with open('bd/speakersMO.json', 'w') as f:
            json.dump(recons_mo, f)
        await interaction.response.send_message("Вы успешно зарегестрировались в Группе Единых Следящих")

class GEIAdd(discord.ui.Modal):
    nick = discord.ui.TextInput(label="Ник администратора")
    discordId = discord.ui.TextInput(label="Id дискорда")
    def __init__(self) -> None:
        super().__init__(title="Добавление администратора", timeout=None)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        if str(self.discordId) in recons_mo:
            await interaction.response.send_message("Данный администратор уже в списке Группы Единых Следящих")
            return
        recons_mo[str(self.discordId)] = {'nick': str(self.nick),'cockie': None,'user_agent': None}
        with open('bd/speakersMO.json', 'w') as f:
            json.dump(recons_mo, f)
        await interaction.response.send_message(f"Администратор {self.nick} успешно добавлен в список Группы Единых Следящих\n<@{self.discordId}> Теперь вы можете использовать /register")

class GEIRemove(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.user_id = user_id

    options = []
    for user_id, user_data in recons_mo.items():
        options.append(discord.SelectOption(label=user_data["nick"], value=user_id))
    @discord.ui.select(placeholder="Выберите администратора", options=options)

    async def select_reason(self, interaction: discord.Interaction, select: discord.ui.Select):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Доступ есть только у того, кто удаляет", ephemeral=True)
            return
        nick = recons_mo[str(select.values[0])]['nick']
        del recons_mo[str(select.values[0])]
        with open('bd/speakersMO.json', 'w') as f:
            json.dump(recons_mo, f)
        await interaction.response.edit_message(content=f"Администратор {nick} удалён из списка Группы Единых Следящих", view=None)

class gei_register_command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("[SYSTEM]: Команда регистрации в ГЕC запущена")

    @app_commands.command(name='register', description="Регистрация в Группу Единых Следящих")
    async def send(self, interaction: discord.Interaction):
        
        if str(interaction.user.id) in recons_mo:
            await interaction.response.send_modal(GEIregister())
        else:
            await interaction.response.send_message("Вас нету в списке Группы Единых Следящих", ephemeral=True)

class gei_add_command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='addtogei', description="Добавление в Группу Единых Следящих")
    async def send(self, interaction: discord.Interaction):
        if interaction.user.guild_permissions.administrator:
            print(interaction.user._permissions)
            await interaction.response.send_modal(GEIAdd())
        else:
            await interaction.response.send_message("Вы не руководитель Группы Единых Следящих", ephemeral=True)

class gei_remove_command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='removegei', description="Удаление из Группы Единых Следящих")
    async def send(self, interaction: discord.Interaction):
        if interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Выберите кого удалить из списка Группы Единых Следящих", view=GEIRemove(interaction.user.id))
        else:
            await interaction.response.send_message("Вы не руководитель Группу Единых Следящих", ephemeral=True)
            

async def setup(bot):
    await bot.add_cog(gei_register_command(bot))
    await bot.add_cog(gei_add_command(bot))
    await bot.add_cog(gei_remove_command(bot))