# main.py
import discord
from discord.ext import commands
import json
import os
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

DATA_FILE = "attendance.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@bot.event
async def on_ready():
    print(f"✅ 로그인됨: {bot.user}")

@bot.command()
async def 출석(ctx):
    user = str(ctx.author.id)
    today = datetime.now().strftime("%Y-%m-%d")
    data = load_data()

    if today not in data:
        data[today] = []

    if user in data[today]:
        await ctx.send(f"{ctx.author.mention} 이미 출석했어요!")
    else:
        data[today].append(user)
        save_data(data)
        await ctx.send(f"{ctx.author.mention} 출석 완료! ✅")

@bot.command(name="출석현황")
async def 출석현황(ctx):
    today = datetime.now().strftime("%Y-%m-%d")
    data = load_data()

    if today not in data or len(data[today]) == 0:
        await ctx.send("오늘 아직 아무도 출석하지 않았어요.")
        return

    names = []
    for user_id in data[today]:
        member = ctx.guild.get_member(int(user_id))
        if member:
            names.append(member.display_name)

    await ctx.send(f"📋 오늘 출석자 ({len(names)}명):\n" + "\n".join(names))

@bot.command(name="출석목록")
async def 출석목록(ctx):
    data = load_data()
    count = {}

    for day in data:
        for user_id in data[day]:
            count[user_id] = count.get(user_id, 0) + 1

    if not count:
        await ctx.send("출석 데이터가 없어요.")
        return

    members = []
    for user_id, num in sorted(count.items(), key=lambda x: x[1], reverse=True):
        member = ctx.guild.get_member(int(user_id))
        if member:
            members.append(f"{member.display_name}: {num}회")

    await ctx.send("🏆 출석 랭킹:\n" + "\n".join(members))

# 여기에 봇 토큰 붙여넣기!
bot.run(os.environ['DISCORD_TOKEN'])
