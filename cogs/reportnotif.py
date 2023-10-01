import asyncio
import discord
from discord.ext import commands
import requests
import bs4
import re
import telebot
import bypass.bypass

coockie = "_ym_uid=1658477733375770370; _ym_d=1691243404; _ga_25SQLLK3B1=GS1.1.1691586289.4.0.1691586289.60.0.0; _gid=GA1.2.114239003.1693833049; xf_tfa_trust=P5WlFYr3j5QLVPFHppt9rvk6sqQHizJW; xf_user=800164%2C8xSYZIR5hxaRD9j52Sfit6pT6IxtbE39RKqajblb; xf_csrf=ZgNorbV7Pvys6Wk0; xf_session=ygogxms03pVOlDsainfjXt7jfBFA9E63; _gat_gtag_UA_175660820_1=1; _ga_KQRCJL2214=GS1.1.1693988528.53.1.1693988654.0.0.0; _ga=GA1.1.1379025495.1669037304"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69"

code = bypass.bypass.bypass(user_agent)
coockie += f"; {code[0]}"
headers = {
        "user-agent": user_agent,
        "cookie": coockie
    }

bot_token = '6012332826:AAFBmAS_HMWIy9udOwsBFscLHyKMFvoUag8'

# Создание объекта бота
bottg = telebot.TeleBot(bot_token)

reportList = []
firstcheck = False

def get_threads(url):
    r = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(r.text, "lxml")
    result = []
    for thread in soup.find_all('div', re.compile('structItem structItem--thread.*')):
        link = object
        unread = False
        closed = False
        pinned = False
        title_element = thread.find_all('div', "structItem-title")[0]
        for el in title_element.find_all("a"):
            if "threads" in el['href']:
                link = el

        matchreportid = re.search(r"/threads/(\d+)/", link['href'].replace("unread", ""))

        if "structItem-status structItem-status--locked" in str(thread):
            closed = True
        if "structItem-status structItem-status--sticky" in str(thread):
            pinned = True
        if "unread" in link['href']:
            unread = True

        creator = thread.find('a').text
        try:
            creator = thread.find('img')['alt']
        except:
            pass

        result.append({
            "title": link.text,
            "link": "https://forum.arizona-rp.com" + link['href'].replace("unread", ""),
            "creator": creator,
            "latest": thread.find('div', re.compile('structItem-cell structItem-cell--latest')).find_all("a")[1].text,
            "closed_date": thread.find('time', re.compile('structItem-latestDate u-dt'))['data-time'],
            "unread": unread,
            "pinned": pinned,
            "closed": closed,
            'id': matchreportid.group(1)
        })
    return result

class checkreport(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("[SYSTEM]: Бот на уведомления о жалобах запущен")
        global firstcheck
        notif_channel = self.bot.get_channel(1148577206591823954)
        while True:
            for thread in get_threads("https://forum.arizona-rp.com/forums/2765/"):
                if not thread['id'] in reportList:
                    reportList.append(thread['id'])
                    if firstcheck:
                        await notif_channel.send(f"<@&1148574777527771136> Новая жалоба\n{thread['link']}: {thread['title']}")
                        bottg.send_message(-902511309, f"Новая жалоба\n{thread['link']}: {thread['title']}")
            for thread in get_threads("https://forum.arizona-rp.com/forums/2766/"):
                if not thread['id'] in reportList:
                    reportList.append(thread['id'])
                    if firstcheck:
                        await notif_channel.send(f"<@&1148574777527771136> Новая жалоба\n{thread['link']}: {thread['title']}")
                        bottg.send_message(-902511309, f"Новая жалоба\n{thread['link']}: {thread['title']}")
            firstcheck = True
            await self.bot.change_presence(status=discord.Status.online, activity=discord.Game('Проверяем жалобы'))
            await asyncio.sleep(300)

async def setup(bot):
    await bot.add_cog(checkreport(bot))