import sqlite3
import secrets
import discord
import random
import asyncio
from discord.ext import commands
import time
from tabulate import tabulate
import os

db = sqlite3.connect('database.db')
sql = db.cursor()

def winrate(wins, games):                           #функция для подсчёта винрейта
        try:
            percent = round((wins/games)*100)
            return str(percent) + '%'
        except ZeroDivisionError:                       #чтобы избежать ошибки, если у игрока 0 игр
            return '0%'

class User(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog user loaded...')

    @commands.command()
    async def stats(self, ctx, member: discord.User = None): #команда _stats (где "_", ваш префикс указаный в начале)
        table = []
        embed = discord.Embed(title='Статистика игрока', colour = 0xFF8C00)
        if member is not None:
            mention = '<@{}>'.format(member.id)
            for row in sql.execute(f"SELECT games, mmr, wins, loses FROM users WHERE id = ?", (member.id,)):
                table.append(row)
            embed.set_thumbnail(url = member.avatar_url)
        else:
            mention = '<@{}>'.format(ctx.author.id)
            for row in sql.execute(f"SELECT games, mmr, wins, loses FROM users WHERE id = ?", (ctx.author.id,)):
                table.append(row)
            embed.set_thumbnail(url = ctx.author.avatar_url)

        embed.add_field(name = 'Никнейм:', value = mention)
        embed.add_field(name = 'Количество игр:', value = table[0][0])
        embed.add_field(name = 'Рейтинг:', value = table[0][1])
        embed.add_field(name = 'Победы:', value = table[0][2])
        embed.add_field(name = 'Поражения:', value = table[0][3])
        embed.add_field(name = 'Процент побед:', value = winrate(table[0][2], table[0][0]))

        await ctx.send(embed = embed)

    @commands.command()
    async def roomrating(self, ctx):                                                                  #рейтинг игроков в руме
        channel = ctx.message.author.voice.channel
        msg = ['```py']
        for member in channel.members:
            id = member.id
            for i in sql.execute(f'SELECT mmr FROM users WHERE id = ?', (id, )):
                mmr = i[0]
            stats = str(member.name) + '\t' + str(mmr)
            msg.append(stats)
        msg.append('```')
        msg = '\n'.join(msg)
        await ctx.send(msg)

def setup(bot):
    bot.add_cog(User(bot))