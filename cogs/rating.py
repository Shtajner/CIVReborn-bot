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

def elo_delta(A,B,s):
        return round(30 * (s - 1 / (1 + 10 ** ((B - A) / 400)))) #где 30, коэффициент k

def elo(args):
    args = list(args)
    new_args = args.copy()
    for i in range(len(args)):
        for j in range(len(args) - i - 1):
            D = elo_delta(args[i], args[j + i + 1], 1)
            new_args[i] += D
            new_args[j + i + 1] -= D
    return new_args

def winrate(wins, games):                           #функция для подсчёта винрейта
    try:
        percent = round((wins/games)*100)
        return str(percent) + '%'
    except ZeroDivisionError:                       #чтобы избежать ошибки, если у игрока 0 игр
        return '0%'

class Rate(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog rating loaded...')

    @commands.command()
    @commands.has_any_role("Администратор 🔧")          #добавить рейта игроку
    async def add(self, ctx, member, amount):
        user = '{}#{}'.format(ctx.message.author.name, ctx.message.author.discriminator)
        member_list = list(str(member))
        member_id = ''.join(member_list[3:-1])
        amount = int(amount)
        for i in sql.execute(f"SELECT mmr FROM users WHERE id = ?", (member_id,)):
            mmr = i[0]
            print(mmr)
        sql.execute(f"UPDATE users SET mmr = {mmr + amount} WHERE id = ?", (member_id,))
        db.commit()
        for i in sql.execute(f"SELECT mmr FROM users WHERE id = ?", (member_id,)):
            new_mmr = int(i[0])
        embed = discord.Embed(colour = 0xFF8C00)
        embed.add_field(name = 'Изменён рейтинг игрока', value = '{}\nБыло: {}\nСтало: {}'.format(member, mmr, new_mmr))
        embed.set_footer(text=user, icon_url=ctx.author.avatar_url)
        await ctx.send(embed = embed)

    @commands.command()
    @commands.has_any_role("Модератор 🔧", "Администратор 🔧")                #посчитать рейтинг за игровую партию
    async def rating(self, ctx, game = None, *members):
        if game == 'mult' or game == 'cc':
            log = self.bot.get_channel(721332224875823155)
            user = '{}#{}'.format(ctx.message.author.name, ctx.message.author.discriminator)
            rating = []
            id_list = []
            for member in members:
                member_list = list(str(member))
                member_id = ''.join(member_list[3:-1])
                for i in sql.execute(f"SELECT mmr FROM users WHERE id = ?", (member_id,)):
                    mmr = i[0]
                    rating.append(mmr)
                id_list.append(member_id)
            new_rating = elo(rating)

            if sql.execute('SELECT id FROM reporting WHERE id = 0').fetchone() is None:
                sql.execute('INSERT INTO reporting VALUES (0, 0, 0)')
                db.commit()
            for i in sql.execute('SELECT max(game_id) FROM reporting'):
                game_id = i[0] + 1

            embed = discord.Embed(title='Рейтинг FFA {} \tID {}'.format(len(id_list), game_id), colour = 0xFF8C00)
            embed.set_footer(text=user, icon_url=ctx.author.avatar_url)
            winner = '<@{}>'.format(id_list[0])
            if game == 'cc':
                embed.add_field(name = 'Итог игры', value = 'Игра была завершена сс в {}'.format(winner))
            else:
                embed.add_field(name = 'Итог игры', value = 'Игра была сыграна до конца и победитель {}'.format(winner))

            for i in range(len(id_list)):                                                               #внесение рейтинга в БД
                sql.execute(f"UPDATE users SET mmr = {new_rating[i]} WHERE id = ?", (id_list[i],))
                db.commit()
                for j in sql.execute(f"SELECT games FROM users WHERE id = ?", (id_list[i],)):
                    games = j[0]
                sql.execute(f"UPDATE users SET games = {games + 1} WHERE id = ?", (id_list[i],))
                db.commit()

                delta = new_rating[i] - rating[i]
                sql.execute(f'INSERT INTO reporting VALUES ({game_id}, {id_list[i]}, {delta})')
                db.commit()
                if delta >= 0:                                                                          #Добавление поражения/луза
                    for j in sql.execute(f"SELECT wins FROM users WHERE id = ?", (id_list[i],)):
                        wins = j[0]
                    sql.execute(f"UPDATE users SET wins = {wins + 1} WHERE id = ?", (id_list[i],))
                    db.commit()
                else:
                    for j in sql.execute(f"SELECT loses FROM users WHERE id = ?", (id_list[i],)):
                        loses = j[0]
                    sql.execute(f"UPDATE users SET loses = {loses + 1} WHERE id = ?", (id_list[i],))
                    db.commit()

                mention = '<@{}>'.format(id_list[i])
                if delta >= 0:
                    embed.add_field(name = '{} место'.format(i+1), value = str(mention) + f"\nБыло: {rating[i]}\nСтало: {new_rating[i]}\nДельта: {delta} ⬆️", inline = False)
                else:
                    embed.add_field(name='{} место'.format(i + 1),
                                    value=str(mention) + f"\nБыло: {rating[i]}\nСтало: {new_rating[i]}\nДельта: {delta} ⬇️", inline = False
                                    )
                embed.set_footer(text=user, icon_url=ctx.author.avatar_url)

            await ctx.send(embed = embed)
            await log.send(embed = embed)
        else:
            await ctx.send('Вы не выбрали тип игры!')

    @commands.command()
    @commands.has_any_role("Администратор 🔧")                             #сброс игры по конкретным ID
    async def reset(self, ctx, game_id):
        embed = discord.Embed(title = f'Сброс игры ID {game_id}', colour = 0xFF8C00)
        num = 0
        while sql.execute("SELECT id FROM reporting WHERE game_id = ?", (game_id,)).fetchone() is not None:
            for i in sql.execute(f"SELECT id, delta FROM reporting where game_id = ?", (game_id,)):
                num += 1
                id = i[0]
                delta = i[1]
                print(id, delta)

                for z in sql.execute("SELECT games FROM users WHERE id = ?", (id,)):
                    games = z[0]
                    sql.execute(f"UPDATE users SET games = {games - 1} WHERE id = ?", (id,))
                    db.commit()

                if delta >= 0:
                    for k in sql.execute(f"SELECT wins FROM users WHERE id = ?", (id,)):
                        wins = k[0]
                        sql.execute(f"UPDATE users SET wins = {wins - 1} WHERE id = ?", (id,))
                        db.commit()
                else:
                    for k in sql.execute(f"SELECT loses FROM users WHERE id = ?", (id,)):
                        loses = k[0]
                        sql.execute(f"UPDATE users SET loses = {loses - 1} WHERE id = ?", (id,))
                        db.commit()

                for j in sql.execute(f"SELECT mmr FROM users WHERE id = ?", (id,)):
                    mmr = j[0]
                    sql.execute(f"UPDATE users SET mmr = {mmr - delta} WHERE id = ?", (id,))
                    db.commit()
                embed.add_field(name=f'Игрок {num}', value=f'<@{id}>\nБыло: {mmr}\nСтало: {mmr - delta}', inline=False)
                sql.execute(f'DELETE FROM reporting WHERE id = ? and game_id = ?', (id, game_id,))
        db.commit()

        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Rate(bot))