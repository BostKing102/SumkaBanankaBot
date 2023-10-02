import requests
import bypass.bypass
from bs4 import BeautifulSoup
import re
import discord
import asyncio
import json
from discord.ext import commands
from logger import *
logger = logging.getLogger("bot")

intents = discord.Intents.all()
intents.message_content = True

coockie = "xf_tfa_trust=Mw3kRYby1QIDtgH7nR3EzjksHNn0LjrU; _ym_uid=1658477733375770370; _ym_d=1694707420; _gid=GA1.2.316968912.1695364393; _ga_25SQLLK3B1=GS1.1.1696008319.5.1.1696009168.21.0.0; xf_notice_dismiss=-1; xf_user=1050943%2CoiJe021zgHSotaKx8ALmdhlFqpaWcwdeZgOrBMoJ; xf_session=ub3bpzViiPH6HpgTxwOxPQdP4qDdv3bU; xf_csrf=U6I7oVR2poPnrdV7; _ga_KQRCJL2214=GS1.1.1696235694.86.1.1696237134.0.0.0; _ga=GA1.2.1805143122.1693988716"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.17"

with open('bd/speakersMO.json', 'r') as f:
    recons_mo = json.load(f)


class setApproved(discord.ui.Modal):
    msg = discord.ui.TextInput(label="Примечание", default="Нету")
    def __init__(self, postid, bbcode, content, author_name, author_id, url, user_agent) -> None:
        super().__init__(title="Одобрение", timeout=None)
        self.value = None
        self.postid = postid
        self.bbcode = bbcode
        self.content = content
        self.author_name = author_name
        self.author_id = author_id
        self.url = url
        self.user_agent = user_agent

    async def on_submit(self, interaction: discord.Interaction) -> None:
        edit_text = f"[QUOTE=\"{self.author_name}, post: {self.postid}, member: {self.author_id}\"]{self.bbcode}[/QUOTE]\n\n[COLOR=rgb(97, 189, 109)][B]Одобрено[/B][/COLOR]\n[B]Примечение:[/B] {self.msg}"
        embed = interaction.message.embeds[0]
        embed.add_field(name='✅ Одобрил', value=interaction.user.mention)
        embed.add_field(name='📄 Примечание', value=self.msg)
        embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
        react_jsbypass = bypass.bypass.bypass(recons_mo[str(interaction.user.id)]['user_agent'])
        cockie = recons_mo[str(interaction.user.id)]['cockie'] + f'; {react_jsbypass[0]}'
        header = {
            "user-agent": recons_mo[str(interaction.user.id)]['user_agent'],
            "cookie": cockie
        }
        statusmsgforum = await send_message(self.url, header, edit_text)
        if statusmsgforum['status'] != "ok":
            await interaction.response.send_message(f"Ошибка: {statusmsgforum}\nДоложите разработчику", ephemeral=True)
        else:
            await interaction.response.edit_message(view=None, embed=embed)

class setRefused(discord.ui.Modal):
    msg = discord.ui.TextInput(label="Отказ")
    def __init__(self, postid, bbcode, content, author_name, author_id, url, user_agent) -> None:
        super().__init__(title="Введите причину отказа", timeout=None)
        self.value = None
        self.postid = postid
        self.bbcode = bbcode
        self.content = content
        self.author_name = author_name
        self.author_id = author_id
        self.url = url
        self.user_agent = user_agent

    async def on_submit(self, interaction: discord.Interaction) -> None:
        edit_text = f"[QUOTE=\"{self.author_name}, post: {self.postid}, member: {self.author_id}\"]{self.bbcode}[/QUOTE]\n\n[COLOR=rgb(184, 49, 47)][B]Отказано[/B][/COLOR]\n[B]Причина:[/B] {self.msg}"
        embed = interaction.message.embeds[0]
        embed.add_field(name='❌ Отказал', value=interaction.user.mention)
        embed.add_field(name='📄 Причина', value=self.msg)
        embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
        react_jsbypass = bypass.bypass.bypass(recons_mo[str(interaction.user.id)]['user_agent'])
        cockie = recons_mo[str(interaction.user.id)]['cockie'] + f'; {react_jsbypass[0]}'
        header = {
            "user-agent": recons_mo[str(interaction.user.id)]['user_agent'],
            "cookie": cockie
        }
        statusmsgforum = await send_message(self.url, header, edit_text)
        if statusmsgforum['status'] != "ok":
            await interaction.response.send_message(f"Ошибка: {statusmsgforum}\nДоложите разработчику", ephemeral=True)
        else:
            await interaction.response.edit_message(view=None, embed=embed)

class CreateTicket(discord.ui.View):
    def __init__(self, postid, bbcode, content, author_name, author_id, url, cookie):
        super().__init__(timeout=None)
        self.value = None
        self.postid = postid
        self.bbcode = bbcode
        self.content = content
        self.author_name = author_name
        self.author_id = author_id
        self.url = url
        self.cookie = cookie

    @discord.ui.button(label="Одобрить", style=discord.ButtonStyle.green, emoji="✅")
    async def SetAllow(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) in recons_mo:
            if recons_mo[str(interaction.user.id)]['cockie'] is not None and recons_mo[str(interaction.user.id)]['user_agent'] is not None:
                await interaction.response.send_modal(setApproved(self.postid, self.bbcode, self.content, self.author_name, self.author_id, self.url, self.cookie))
            else:
                await interaction.response.send_message("Вы не зарегестрированы в системе")
        else:
            await interaction.response.send_message("Ошибка доступа: Вас нет в списке следящих МО.")


    @discord.ui.button(label="Отказать", style=discord.ButtonStyle.red, emoji="❎")
    async def setDeny(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) in recons_mo:
            if recons_mo[str(interaction.user.id)]['cockie'] is not None and recons_mo[str(interaction.user.id)]['user_agent'] is not None:
                await interaction.response.send_modal(setRefused(self.postid, self.bbcode, self.content, self.author_name, self.author_id, self.url, self.cookie))
            else:
                await interaction.response.send_message("Вы не зарегестрированы в системе")
        else:
            await interaction.response.send_message("Ошибка доступа: Вас нет в списке следящих МО.")

def html_to_text(html):
    # Используем BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(html, 'html.parser')

    for br in soup.find_all("br"):
        br.extract()

    # Извлекаем текст без HTML тегов
    text = soup.get_text(separator=' ').strip()

    # Извлекаем ссылки из HTML с помощью регулярного выражения
    links = re.findall(r'href=["\'](https?://.*?)(?=["\'])', html)

    return text, links

async def send_message(url, custom_headers, message):
    try:
        r = requests.get(url, headers=custom_headers)
        soup = BeautifulSoup(r.text, "lxml")
        form = soup.find_all("form")[1]

        action = "https://forum.arizona-rp.com" + form['action']
        token = re.compile("name=\"_xfToken\" value=\"(.*)\" />").findall(r.text)[0]
        json = {
            "message": message,
            "_xfToken": token,
            "last_date": form.find_all("input", {"name": "last_date"})[0]['value'],
            "last_known_date": form.find_all("input", {"name": "last_known_date"})[0]['value'],
            "_xfResponseType": "json"
        }
        status = requests.post(action, data=json, headers=custom_headers)
        return status.json()
    except Exception as e:
        return {'status': 'fail', 'message': e}


def html_to_bbcode_with_links(html):
    # Создаем объект BeautifulSoup для разбора HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Находим все элементы div с классом "bbWrapper"
    div_elements = soup.find_all('div', class_='bbWrapper')

    for div_element in div_elements:
        link_element = div_element.find('a', class_='link--external') or div_element.find('a', class_='link--internal')

        if link_element:
            href = link_element.get('href')
            text = link_element.text
            bbcode = f'{div_element.text.replace(text, f"[url={href}]{text}[/url]")}'
            div_element.replace_with(bbcode)

    # Возвращаем обновленный текст
    return str(soup.getText())

code = bypass.bypass.bypass(user_agent)
coockie += f"; {code[0]}"
headers = {
    "user-agent": user_agent,
    "cookie": coockie
}

firstCheck = False

#"910919635468181595": {
#        "nick": "Raymond_Kenney",
#        "cockie": "xf_tfa_trust=Mw3kRYby1QIDtgH7nR3EzjksHNn0LjrU; _gid=GA1.2.1171959083.1694434689; xf_user=1050943%2C3z-TerjjRMyQpztkDU6wbqpBZFrXgll-Xd1Lvo15; xf_session=d40Gtn14M7ps6hpQGA0fzW4q4pyu74ac; xf_csrf=FqUms5CZcmiiT3tD; _ga_KQRCJL2214=GS1.1.1694508711.12.1.1694515037.0.0.0; _ga=GA1.2.1805143122.1693988716; _gat_gtag_UA_175660820_1=1",
#        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76"
#    },

cheked_posts = []

async def checkAb(url, channelId, bot):
    antiblat_thread = requests.get(url + "page-9999", headers=headers)
    last_page = re.search(r"page-(\d+)", antiblat_thread.text).group(1)
    if int(last_page) != 9999:
        antiblat_thread_last = requests.get(url, headers=headers)
    else:
        antiblat_thread_last = requests.get(f"{url}page-{last_page}", headers=headers)
    antiblat_html_last = BeautifulSoup(antiblat_thread_last.text, "lxml")
    for post in antiblat_html_last.find_all("article", re.compile("message message--post js-post js-inlineModContainer")):
        postid = re.search('post-(\d+)', post.find('span', re.compile('u-anchorTarget'))['id']).group(1)
        links_content = html_to_text(str(post.find('div', 'bbWrapper')))
        author_name = post['data-author']
        author_id = post.find('a', "avatar avatar--m")['data-user-id']
        user_type = post.find('strong').text
        if postid not in cheked_posts:
            cheked_posts.append(postid)
            if firstCheck and user_type == "Пользователь":
                bbcode = html_to_bbcode_with_links(str(post.find('div', 'bbWrapper')))
                content = f"```{links_content[0]} \n {''.join(links_content[1])}```"
                view = CreateTicket(postid, bbcode, content, author_name, author_id, url, user_agent)
                anti_blat_check_channel = bot.get_channel(int(channelId))
                embed = discord.Embed(title=f'👮 Антиблат№{postid}', url=f'{url}post-{postid}')
                embed.add_field(name="🗨️ Содержание", value="```" + links_content[0] + "```", inline=False)
                embed.add_field(name="🔗 Ссылки", value='\n'.join(links_content[1]), inline=False)
                embed.set_footer(text="SumkaBanankaBot", icon_url=bot.user.avatar.url)
                await anti_blat_check_channel.send("<@&1145744379252834376> пришел новый антиблат", view=view, embed=embed)
    
    if int(last_page) != 9999:
        antiblat_thread_perv = requests.get(f"{url}page-{int(last_page) - 1}", headers=headers)
        antiblat_html_perv = BeautifulSoup(antiblat_thread_perv.text, "lxml")
        for post in antiblat_html_perv.find_all("article", re.compile("message message--post js-post js-inlineModContainer")):
            postid = re.search('post-(\d+)', post.find('span', re.compile('u-anchorTarget'))['id']).group(1)
            links_content = html_to_text(str(post.find('div', 'bbWrapper')))
            author_name = post['data-author']
            author_id = post.find('a', "avatar avatar--m")['data-user-id']
            user_type = post.find('strong').text
            if postid not in cheked_posts:
                cheked_posts.append(postid)
                if firstCheck and user_type == "Пользователь":
                    bbcode = html_to_bbcode_with_links(str(post.find('div', 'bbWrapper')))
                    content = f"```{links_content[0]} \n {''.join(links_content[1])}```"
                    view = CreateTicket(postid, bbcode, content, author_name, author_id, url, user_agent)
                    anti_blat_check_channel = bot.get_channel(int(channelId))
                    embed = discord.Embed(title=f'👮 Антиблат№{postid}', url=f'{url}post-{postid}')
                    embed.add_field(name="🗨️ Содержание", value="```" + links_content[0] + "```", inline=False)
                    embed.add_field(name="🔗 Ссылки", value='\n'.join(links_content[1]), inline=False)
                    embed.set_footer(text="SumkaBanankaBot", icon_url=bot.user.avatar.url)
                    await anti_blat_check_channel.send("<@&1145744379252834376> пришел новый антиблат", view=view, embed=embed)

cheked_themes = [
    {"url": "https://forum.arizona-rp.com/threads/6614681/", "id": 1149246108846010479}, #Антиблат МО
    {"url": "https://forum.arizona-rp.com/threads/6615786/", "id": 1155931375187263549}, #Антиблат МЗ
]

class checkantiblat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("[SYSTEM]: Служба проверки антиблата запущена")
        global firstCheck, user_agent
        await self.bot.get_channel(1151477151003070524).send("БОТ ЗАПУЩЕН")
        while True:
            for theme in cheked_themes:
                await checkAb(theme['url'], theme['id'], self.bot)
                await self.bot.change_presence(status=discord.Status.online, activity=discord.Game('Проверяем АнтиБлат'))
                await asyncio.sleep(10)
            firstCheck = True
            await asyncio.sleep(1200)
        
async def setup(bot):
    await bot.add_cog(checkantiblat(bot))