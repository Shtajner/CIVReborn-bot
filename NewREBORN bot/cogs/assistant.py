import sqlite3
import secrets
import discord
import random
import asyncio
from discord.ext import commands
import time
from tabulate import tabulate
import os

class Assistant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog assistant loaded...')


    @commands.command()
    @commands.has_permissions(administrator = True)
    async def clear(ctx, amount = 50):
        await ctx.channel.purge(limit = amount)

    @commands.command()
    @commands.has_any_role("Модератор 🔧", "Администратор 🔧")
    async def newrule(self, ctx, *message):
        message = ' '.join(message)
        embed = discord.Embed(description = message, colour = 0x505050)
        user = '{}#{}'.format(ctx.message.author.name, ctx.message.author.discriminator)
        channel = bot.get_channel(699002878701993995)

        embed.set_footer(text = user, icon_url = ctx.author.avatar_url)

        msg = await channel.send(embed=embed)
        await msg.add_reaction('✅')
        await msg.add_reaction('❎')
        time.sleep(5)
        await ctx.message.delete()

    @commands.command()
    async def begin(self, ctx):
        msg = await ctx.send('**Рейтинговая игра:** ✅, ❎')
        reactions = ['✅', '❎']
        for reaction in reactions:
            await msg.add_reaction(reaction)

        msg = await ctx.send('**Карта:** 🇵 = Пангея, 🇴 = Озёра, 🗾 = Континенты, 🏝️ = Архипелаги, 7️⃣ = Семь Морей, ➕ - Пангея +')
        reactions = ['🇵', '🇴', '🗾', '🏝️', '7️⃣', '➕']
        for reaction in reactions:
            await msg.add_reaction(reaction)

        msg = await ctx.send('**Возраст мира:** 🗻 = Новый,  🌄 = Стандартный,  🏳️‍🌈 = Старый')
        reactions = ['🗻', '🌄', '🏳️‍🌈']
        for reaction in reactions:
            await msg.add_reaction(reaction)

        msg = await ctx.send('**Стихийные бедствия:** 2⃣ , 3⃣ , 4⃣ ')
        reactions = ['2⃣', '3⃣', '4⃣']
        for reaction in reactions:
            await msg.add_reaction(reaction)

        msg = await ctx.send('**Бонусные ресурсы:** 🇸 = Стандартные, 🇮 = Изобильные')
        reactions = ['🇸', '🇮']
        for reaction in reactions:
            await msg.add_reaction(reaction)

        msg = await ctx.send('**Стратресы:** 🇸 = Standard, 🇬 = Spawn Guaranteed')
        reactions = ['🇸', '🇬']
        for reaction in reactions:
            await msg.add_reaction(reaction)

        msg = await ctx.send('**Баны по нации:** ✅, ❎')
        reactions = ['✅', '❎']
        for reaction in reactions:
            await msg.add_reaction(reaction)

        msg = await ctx.send('**Общение с игроками:** 📣 = Публичное, ✉️ = Любое')
        reactions = ['📣', '✉']
        for reaction in reactions:
            await msg.add_reaction(reaction)

        msg = await ctx.send('**Максимум дружб/союзов:** 1️⃣, 2️⃣, ♾️')
        reactions = ['1️⃣', '2️⃣', '♾️']
        for reaction in reactions:
            await msg.add_reaction(reaction)

        msg = await ctx.send('**Обмен/подарки золотом:** ✅, ❎ 🇫 = Только между друзьями/союзниками 🇦 = Только между союзниками')
        reactions = ['✅', '❎', '🇫', '🇦']
        for reaction in reactions:
            await msg.add_reaction(reaction)

        msg = await ctx.send('**Обмен/подарки стратресами:** ✅, ❎ 🇫 = Только между друзьями/союзниками 🇦 = Только между союзниками')
        reactions = ['✅', '❎', '🇫', '🇦']
        for reaction in reactions:
            await msg.add_reaction(reaction)

        embed = discord.Embed(description='**Сделайте реакцию нации, которую хотите забанить, под этим сообщением**',
                              colour=0x8b00ff)
        await ctx.send(embed=embed)

        time.sleep(5)
        await ctx.message.delete()

    @commands.command()
    async def draftffa(self, ctx, *bans):
        leaders = {"<:Australia:701066628523098183>": 'Австралия <:Australia:701066628523098183> Джон Кэртин',
               "<:America:701066550412836894>": 'Америка <:America:701066550412836894> Теодор Рузвельт',
               "<:EnglandV:701066628489674772>": 'Англия <:EnglandV:701066628489674772> Виктория',
               "A<:EnglandV:701066628489674772>": 'Англия <:EnglandV:701066628489674772> Алиенора Аквитанская',
               "<:Arabia:701066550442065970>": 'Аравия <:Arabia:701066550442065970> Саладин',
               "<:Aztecs:701066550169436302>": 'Ацтеки <:Aztecs:701066550169436302> Монтесума',
               "<:Brazil:701066699537121281>": 'Бразилия <:Brazil:701066699537121281> Педру II',
               "<:Hungary:701066628674224128>": 'Венгрия <:Hungary:701066628674224128> Матьяш I',
               "<:Germany:701066628653252658>": 'Германия <:Germany:701066628653252658> Фридрих Барбаросса',
               "<:GreeceG:701900974108835900>": 'Греция <:GreeceG:701900974108835900> Горго',
               "<:GreeceP:701900991460540648>": 'Греция <:GreeceP:701900991460540648> Перикл',
               "<:Georgia:701066628518903848>": 'Грузия <:Georgia:701066628518903848> Тамара',
               "<:Egypt:701066550265774162>": 'Египет <:Egypt:701066550265774162> Клеопатра',
               "<:Zulu:701066699553767465>": 'Зулусы <:Zulu:701066699553767465> Чака',
               "<:IndiaG:701066628640800838>": 'Индия <:IndiaG:701066628640800838> Ганди',
               "<:IndiaC:701901750503997501>": 'Индия <:IndiaC:701901750503997501> Чандрагупта',
               "<:Indonesia:701066550425288754>": 'Индонезия <:Indonesia:701066550425288754> Трибхувана',
               "<:Inca:701066628737007666>": 'Инки <:Inca:701066628737007666> Пачакутек',
               "<:Spain:701066699704893460>": 'Испания <:Spain:701066699704893460> Филипп II',
               "<:Canada:701066699557961829>": 'Канада <:Canada:701066699557961829> Уилфрид Лорье',
               "<:China:701066550433677382>": 'Китай <:China:701066550433677382> Цинь Шихуанди',
               "<:Kongo:701066628661641293>": 'Конго <:Kongo:701066628661641293> Мвемба а Нзинга',
               "<:Korea:701066550232219801>": 'Корея <:Korea:701066550232219801> Сондок',
               "<:Cree:701066550504980480>": 'Кри <:Cree:701066550504980480> Паундмейкер',
               "<:Khmer:701066628150067302>": 'Кхмеры <:Khmer:701066628150067302> Джайаварман VII',
               "<:Macedonia:701066628540006470>": 'Македония <:Macedonia:701066628540006470> Александр',
               "<:Mali:701066699490852914>": 'Мали <:Mali:701066699490852914> Манса Муса',
               "<:Maori:701066699801231460>": 'Маори <:Maori:701066699801231460> Купе',
               "<:Mongolia:701066699482464276>": 'Монголия <:Mongolia:701066699482464276> Чингисхан',
               "<:Mapuche:701066724036050974>": 'Мапуче <:Mapuche:701066724036050974> Лаутаро',
               "<:Nederlands:701066724111548476>": 'Нидерланды <:Nederlands:701066724111548476> Вильгельмина',
               "<:Norway:701066723721216011>": 'Норвегия <:Norway:701066723721216011> Харальд Суровый',
               "<:Nubia:701066699700699136>": 'Нубия <:Nubia:701066699700699136> Аманиторе',
               "<:Ottoman:701066699230674976>": 'Оттоманы <:Ottoman:701066699230674976> Сулейман',
               "<:Persia:701066723713089608>": 'Персия <:Persia:701066723713089608> Кир',
               "<:Poland:701066699486789752>": 'Польша <:Poland:701066699486789752> Ядвига',
               "<:Rome:701066699499372615>": 'Рим <:Rome:701066699499372615> Траян',
               "<:Russia:701066723868147734>": 'Россия <:Russia:701066723868147734> Петр Великий',
               "<:Scythia:701066699608162334>": 'Скифия <:Scythia:701066699608162334> Томирис',
               "<:Phoenicia:701066628141678623>": 'Финикия <:Phoenicia:701066628141678623> Дидона',
               "<:FranceM:701066550051864628>": 'Франция <:FranceM:701066550051864628> Екатерина Медичи',
               "A<:FranceM:701066550051864628>": 'Франция <:FranceM:701066550051864628> Алиенора Аквитанская',
               "<:Sweden:701066699608293376>": 'Швеция <:Sweden:701066699608293376> Кристина',
               "<:Scotland:701066724031594566>": 'Шотландия <:Scotland:701066724031594566> Роберт I Брюс',
               "<:Sumeria:701066699516018688>": 'Шумерия <:Sumeria:701066699516018688> Гильгамеш',
               "<:Japan:701066628498063380>": 'Япония <:Japan:701066628498063380> Ходзе Токимунэ',
               "<:Maya:713789628829663283>": 'Майя <:Maya:713789628829663283> Госпожа Шестого Неба',
               "<:Colombia:713789628590850149>": 'Колумбия <:Colombia:713789628590850149> Симон Боливар',
               "<:Ethiopia:736271149159284807>": 'Эфиопия <:Ethiopia:736271149159284807> Менелик II',
               "R<:America:701066550412836894>": 'Америка <:America:701066550412836894> Мужественный всадник Тедди',
               "M<:FranceM:701066550051864628>": 'Франция <:FranceM:701066550051864628> Великолепная Екатерина',
               "<:Byzantium:759396923382956043>": 'Византия <:Byzantium:759396923382956043> Василий II',
               "<:Gaul:759396911206629386>": 'Галлия <:Gaul:759396911206629386> Амбиорикс'
               }
        num_draft = 3
        ban_list = []
        players_list = []
        channel = ctx.message.author.voice.channel
        user = '{}#{}'.format(ctx.message.author.name, ctx.message.author.discriminator)
        for members in channel.members:                                                 #Получение списка игроков в комнате
            player = '{}#{}'.format(members.name, members.discriminator)
            players_list.append(player)
        if len(leaders) < len(players_list) * num_draft + len(bans):                    #Проверка на количество наций
            error_embed = discord.Embed(description='Ошибка: Недостаточно наций для драфта!')
            await ctx.send(embed = error_embed)
            return
        else:
            for i in range(len(bans)):                                                  #Удаление забаненных наций из словаря
                key = bans[i]
                if key in leaders:
                    ban_list.append(leaders[key])
                    del leaders[key]

        embed = discord.Embed(title = 'Драфт FFA')
        embed.set_thumbnail(url = 'https://i.gifer.com/origin/46/46bd808cbf7e6fa994d5e44ee271b156.gif')
        bans_str = ' \n '.join(ban_list)
        if bans_str == "":
            embed.add_field(name = 'Список банов:', value = 'Без банов', inline = False)
        else:
            embed.add_field(name = 'Список банов:', value = bans_str, inline = False)
        for i in range(len(players_list)):
            draft = []
            for _ in range(num_draft):
                random_key = random.choice(list(leaders.keys()))
                draft.append(leaders[random_key])
                del leaders[random_key]
            embed.add_field(name = players_list[i], value = ' \n '.join(draft), inline = False)
        embed.set_footer(text=user, icon_url=ctx.author.avatar_url)
        await ctx.send(embed = embed)
        time.sleep(5)
        await ctx.message.delete()

    @commands.command()
    async def coinflip(self, ctx):
        user = '{}#{}'.format(ctx.message.author.name, ctx.message.author.discriminator)
        coin = secrets.randbelow(2)
        if coin == 0:
            coin_embed = discord.Embed(title='Решка', colour=0x505050)
            coin_embed.set_image(url="https://miranimacii.ru/_ph/23/997997674.gif")
            coin_embed.set_footer(text=user, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=coin_embed)
        else:
            coin_embed = discord.Embed(title = 'Орёл', colour = 0x4d7198)
            coin_embed.set_image(url = "https://miranimacii.ru/_ph/23/997997674.gif")
            coin_embed.set_footer(text=user, icon_url = ctx.author.avatar_url)
            await ctx.send(embed=coin_embed)
        time.sleep(5)
        await ctx.message.delete()

    @commands.command()
    async def election(self, ctx, *message):
        user = '{}#{}'.format(ctx.message.author.name, ctx.message.author.discriminator)
        message = ' '.join(message)
        channel = bot.get_channel(699002644093731005)
        embed = discord.Embed(description = message, colour = 0xFFD900)
        embed.set_footer(text = user, icon_url = ctx.author.avatar_url)
        if channel:
            msg = await channel.send(embed = embed)
        await msg.add_reaction('✅')
        await msg.add_reaction('❎')
        time.sleep(5)
        await ctx.message.delete()

    @commands.command()
    async def vote(self, ctx, *message):
        message = ' '.join(message)
        user = '{}#{}'.format(ctx.message.author.name, ctx.message.author.discriminator)
        embed = discord.Embed(description=message, colour=0xFFD900)
        embed.set_footer(text=user, icon_url=ctx.author.avatar_url)
        msg = await ctx.send(embed = embed)
        await msg.add_reaction('✅')
        await msg.add_reaction('❎')
        time.sleep(5)
        await ctx.message.delete()

    @commands.command()
    async def proposal(self, ctx, *message):
        user = '{}#{}'.format(ctx.message.author.name, ctx.message.author.discriminator)
        message = ' '.join(message)
        channel = bot.get_channel(701526420962410626)
        embed = discord.Embed(description = message, colour = 0xFFD900)
        embed.set_footer(text=user, icon_url=ctx.author.avatar_url)
        if channel:
            msg = await channel.send(embed=embed)
        await msg.add_reaction('✅')
        await msg.add_reaction('❎')
        time.sleep(5)
        await ctx.message.delete()

    @commands.command()
    async def team(self, ctx):
        players_list = []
        channel = ctx.message.author.voice.channel
        user = '{}#{}'.format(ctx.message.author.name, ctx.message.author.discriminator)
        embed = discord.Embed(title='Рандомное деление на 2 команды:', colour=0x57ff57)
        embed.set_thumbnail(url='https://irp-cdn.multiscreensite.com/e2c60357/dms3rep/multi/flags-animation.gif')
        embed.set_footer(text=user, icon_url=ctx.author.avatar_url)
        for members in channel.members:  # Получение списка игроков в комнате
            player = '{}#{}'.format(members.name, members.discriminator)
            players_list.append(player)
        k = len(players_list)
        for i in range(2):
            team = []
            for j in range(k // 2):
                team_number = 'Команда ' + str(i + 1)
                teammate = random.choice(players_list)
                team.append(teammate)
                players_list.remove(teammate)
                team_str = ' \n '.join(team)
            embed.add_field(name=team_number, value=team_str)
        await ctx.send(embed=embed)
        time.sleep(5)
        await ctx.message.delete()

    @commands.command()
    async def draftteam(self, ctx):
        early_war = {"<:Macedonia:701066628540006470>": 'Македония <:Macedonia:701066628540006470> Александр',
                         "<:Persia:701066723713089608>": 'Персия <:Persia:701066723713089608> Кир',
                         "<:Scythia:701066699608162334>": 'Скифия <:Scythia:701066699608162334> Томирис',
                         "<:Nubia:701066699700699136>": 'Нубия <:Nubia:701066699700699136> Аманиторе',
                         "<:Cree:701066550504980480>": 'Кри <:Cree:701066550504980480> Паундмейкер',
                         "<:IndiaC:701901750503997501>": 'Индия <:IndiaC:701901750503997501> Чандрагупта'}
        religion = {"<:Arabia:701066550442065970>": 'Аравия <:Arabia:701066550442065970> Саладин',
                    "<:Russia:701066723868147734>": 'Россия <:Russia:701066723868147734> Петр Великий',
                    "<:IndiaG:701066628640800838>": 'Индия <:IndiaG:701066628640800838> Ганди',
                    "<:Khmer:701066628150067302>": 'Кхмеры <:Khmer:701066628150067302> Джайаварман VII',
                    "<:Poland:701066699486789752>": 'Польша <:Poland:701066699486789752> Ядвига',
                    "<:Canada:701066699557961829>": 'Канада <:Canada:701066699557961829> Уилфрид Лорье',
                    "<:Georgia:701066628518903848>": 'Грузия <:Georgia:701066628518903848> Тамара'}
        houseworking = {"<:Mali:701066699490852914>": 'Мали <:Mali:701066699490852914> Манса Муса',
                        "<:GreeceG:701900974108835900>": 'Греция <:GreeceG:701900974108835900> Горго',
                        "<:GreeceP:701900991460540648>": 'Греция <:GreeceP:701900991460540648> Перикл',
                        "<:Germany:701066628653252658>": 'Германия <:Germany:701066628653252658> Фридрих Барбаросса',
                        "<:FranceA:701903277582712942>": 'Франция <:FranceA:701903277582712942> Алиенора Аквитанская',
                        "<:Australia:701066628523098183>": 'Австралия <:Australia:701066628523098183> Джон Кэртин',
                        "<:Sweden:701066699608293376>": 'Швеция <:Sweden:701066699608293376> Кристина',
                        "<:Inca:701066628737007666>": 'Инки <:Inca:701066628737007666> Пачакутек',
                        "<:China:701066550433677382>": 'Китай <:China:701066550433677382> Цинь Шихуанди',
                        "<:Scotland:701066724031594566>": 'Шотландия <:Scotland:701066724031594566> Роберт I Брюс',
                        "<:Korea:701066550232219801>": 'Корея <:Korea:701066550232219801> Сондок',
                        "<:Brazil:701066699537121281>": 'Бразилия <:Brazil:701066699537121281> Педру II',
                        "<:Nederlands:701066724111548476>": 'Нидерланды <:Nederlands:701066724111548476> Вильгельмина',
                        "<:Maya:713789628829663283>": 'Майя <:Maya:713789628829663283> Госпожа Шестого Неба'}
        sea = {"<:EnglandV:701066628489674772>": 'Англия <:EnglandV:701066628489674772> Виктория',
               "<:EnglandA:701896039551991938>": 'Англия <:EnglandA:701896039551991938> Алиенора Аквитанская',
               "<:Phoenicia:701066628141678623>": 'Финикия <:Phoenicia:701066628141678623> Дидона',
               "<:Indonesia:701066550425288754>": 'Индонезия <:Indonesia:701066550425288754> Трибхувана',
               "<:Norway:701066723721216011>": 'Норвегия <:Norway:701066723721216011> Харальд Суровый',
               }
        universal = {"<:Rome:701066699499372615>": 'Рим <:Rome:701066699499372615> Траян',
                     "<:Kongo:701066628661641293>": 'Конго <:Kongo:701066628661641293> Мвемба а Нзинга',
                     "<:Mapuche:701066724036050974>": 'Мапуче <:Mapuche:701066724036050974> Лаутаро',
                     "<:Japan:701066628498063380>": 'Япония <:Japan:701066628498063380> Ходзе Токимунэ',
                     "<:FranceM:701066550051864628>": 'Франция <:FranceM:701066550051864628> Екатерина Медичи',
                     "<:America:701066550412836894>": 'Америка <:America:701066550412836894> Теодор Рузвельт',
                     "<:Egypt:701066550265774162>": 'Египет <:Egypt:701066550265774162> Клеопатра',
                     "<:Maori:701066699801231460>": 'Маори <:Maori:701066699801231460> Купе',
                     "<:Spain:701066699704893460>": 'Испания <:Spain:701066699704893460> Филипп II',
                     "<:Sumeria:701066699516018688>": 'Шумерия <:Sumeria:701066699516018688> Гильгамеш',
                     }
        mid_or_late_war = {"<:Aztecs:701066550169436302>": 'Ацтеки <:Aztecs:701066550169436302> Монтесума',
                           "<:Hungary:701066628674224128>": 'Венгрия <:Hungary:701066628674224128> Матьяш I',
                           "<:Zulu:701066699553767465>": 'Зулусы <:Zulu:701066699553767465> Чака',
                           "<:Mongolia:701066699482464276>": 'Монголия <:Mongolia:701066699482464276> Чингисхан',
                           "<:Ottoman:701066699230674976>": 'Оттоманы <:Ottoman:701066699230674976> Сулейман',
                           "<:Colombia:713789628590850149>": 'Колумбия <:Colombia:713789628590850149> Симон Боливар'
                           }
        ban_list = []
        embed = discord.Embed(title='Драфт Teamers', value=', '.join(ban_list))
        for j in range(2):
            draft = []
            for _ in range(2):
                random_key = random.choice(list(early_war.keys()))
                draft.append(early_war[random_key])
                del early_war[random_key]

            for _ in range(2):
                random_key = random.choice(list(religion.keys()))
                draft.append(religion[random_key])
                del religion[random_key]

            for _ in range(2):
                random_key = random.choice(list(sea.keys()))
                draft.append(sea[random_key])
                del sea[random_key]

            for _ in range(2):
                random_key = random.choice(list(universal.keys()))
                draft.append(universal[random_key])
                del universal[random_key]

            for _ in range(2):
                random_key = random.choice(list(mid_or_late_war.keys()))
                draft.append(mid_or_late_war[random_key])
                del mid_or_late_war[random_key]

            for _ in range(2):
                random_key = random.choice(list(houseworking.keys()))
                draft.append(houseworking[random_key])
                del houseworking[random_key]
            embed.add_field(name=f'Команда {j + 1}', value='\n'.join(draft), inline=False)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Assistant(bot))