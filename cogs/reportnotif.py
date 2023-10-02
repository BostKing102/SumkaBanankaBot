import asyncio
import discord
from discord.ext import commands
import requests
import bs4
import re
import telebot
import bypass.bypass

coockie = "xf_tfa_trust=Mw3kRYby1QIDtgH7nR3EzjksHNn0LjrU; _ym_uid=1658477733375770370; _ym_d=1694707420; _gid=GA1.2.316968912.1695364393; _ga_25SQLLK3B1=GS1.1.1696008319.5.1.1696009168.21.0.0; xf_csrf=ok2-4jvSCcB9gsdw; xf_notice_dismiss=-1; xf_user=1050943%2CoiJe021zgHSotaKx8ALmdhlFqpaWcwdeZgOrBMoJ; xf_session=xWpDZUAgjW-68Z4ZGhrZcrrwpdxo_HCD; _ga_KQRCJL2214=GS1.1.1696183571.85.1.1696183645.0.0.0; _ga=GA1.1.1805143122.1693988716"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.17"

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