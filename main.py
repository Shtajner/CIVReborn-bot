import sqlite3
import secrets
import discord
import random
import asyncio
from discord.ext import commands
import time
from tabulate import tabulate
import os

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)
TOKEN = 'NzEzNzA0MTcwMjkyNjQxODUz.XsvEjA.wd3t_151fHX7KeBcU_68BGvXhB8'
bot.remove_command('help')

db = sqlite3.connect('database.db')
sql = db.cursor()


sql.execute("""CREATE TABLE IF NOT EXISTS "users" (
    "id"    INT,
    "games"     INT,
    "mmr"       INT,
    "wins"       INT,
    "loses"     INT 
)""")

db.commit()

sql.execute("""CREATE TABLE IF NOT EXISTS "reporting" (
    "game_id"    INT,
    "id"        INT,
    "delta"     INT
)""")

db.commit()

sql.execute("""CREATE TABLE IF NOT EXISTS "clans" (
    "name_id"    INT,
    "members_id"        INT,
    "description"     TEXT,
    "URL"   TEXT
)""")

@bot.event
async def on_ready():
    print("Bot Has been runned")            # сообщение о готовности
    roles_names = ["1", "2", "3", "4", "5", "6", "7", "8"]
    for guild in bot.guilds:
        for member in guild.members:
            if sql.execute(f"SELECT id FROM users where id={member.id}").fetchone() is None:
                sql.execute(f"""INSERT INTO users VALUES ({member.id}, 0, 1000, 0, 0)""")
            else:
                pass
            db.commit()
            for role_name in roles_names:
                role = discord.utils.get(member.guild.roles, name = role_name)
                if role in member.roles:
                    await member.remove_roles(role)                                                                #сбрасывает роли, чтобы заново дать потом

            for i in sql.execute(f"SELECT mmr FROM users WHERE id = ?", (member.id,)):                              #цикл обновляет роли игроков
                mmr = i[0]
                if mmr <= 899:
                    role = discord.utils.get(member.guild.roles, name="⚔️ Поселенец")
                    await member.add_roles(role)
                elif 900 <= mmr <= 999:
                    role = discord.utils.get(member.guild.roles, name="⚔️ Вождь")
                    await member.add_roles(role)
                elif 1000 <= mmr <= 1099:
                    role = discord.utils.get(member.guild.roles, name="⚔️ Военачальник")
                    await member.add_roles(role)
                elif 1100 <= mmr <= 1299:
                    role = discord.utils.get(member.guild.roles, name="⚔️ Князь")
                    await member.add_roles(role)
                elif 1300 <= mmr <= 1499:
                    role = discord.utils.get(member.guild.roles, name="⚔️ Король")
                    await member.add_roles(role)
                elif 1500 <= mmr <= 1699:
                    role = discord.utils.get(member.guild.roles, name="⚔️ Император")
                    await member.add_roles(role)
                elif 1700 <= mmr <= 1899:
                    role = discord.utils.get(member.guild.roles, name="⚔️ Бессмертный")
                    await member.add_roles(role)
                elif mmr >= 1900:
                    role = discord.utils.get(member.guild.roles, name="⚔️ Божество")
                    await member.add_roles(role)

@bot.event
async def on_member_join(member):
    sql.execute(f"SELECT id FROM users where id={member.id}")                                                                #все также, существует ли участник в БД
    if sql.fetchone()==None:                                                                                                 #Если не существует
        sql.execute("INSERT INTO users VALUES ({}, 0, 1000, 0, 0)".format(member.id))       #вводит все данные об участнике в БД
    else:                                                                                                                       #Если существует
        pass
    db.commit()         #применение изменений в БД


@bot.command()
async def load(ctx, extension):
    if ctx.author.id == 283665658565230592:
        bot.load_extension(f'cogs.{extension}')
        await ctx.send('Коги загружены')
    else:
        await ctx.send('Вы не разработчик бота')

@bot.command()
async def unload(ctx, extension):
    if ctx.author.id == 283665658565230592:
        bot.unload_extension(f'cogs.{extension}')
        await ctx.send('Коги загружены')
    else:
        await ctx.send('Вы не разработчик бота')

@bot.command()
async def reload(ctx, extension):
    if ctx.author.id == 283665658565230592:
        bot.unload_extension(f'cogs.{extension}')
        bot.load_extension(f'cogs.{extension}')
        await ctx.send('Коги загружены')
    else:
        await ctx.send('Вы не разработчик бота')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(TOKEN)