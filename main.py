from discord.ext import commands
from database import DBase
import json
import discord
import asyncio

bot = commands.Bot(command_prefix='!')

@bot.command(pass_context=True)
async def role(ctx, role="None"):

    user = str(ctx.message.author)
    role = role.lower().title()
    msg_res = None

    if role == "Titan" or role == "Warlock" or role == "Hunter":
        with DBase() as db:
            db.update_roster(user, role)
        msg_res = await bot.say(ctx.message.author.mention + ": Your role has been updated!")
    else:
        msg_res = await bot.say(ctx.message.author.mention + ": Oops! Role must be one of: Titan, Hunter, Warlock")

    if ctx.message.channel.type is not discord.ChannelType.private:
        await asyncio.sleep(3)
        await bot.delete_message(msg_res)
        await bot.delete_message(ctx.message)


@bot.command()
async def roster():

    with DBase() as db:
        roster = db.get_roster()
        if roster:

            message = "```\n"
            for row in roster:
                message += row[0].split("#")[0]
                spaces = 17 - len(row[0].split("#")[0])
                for _ in range (0, spaces):
                    message += " "
                message += row[1] + "\n"
            message += "```"

            embed_msg = discord.Embed(title="Destiny 2 Pre Launch Roster", description=message, color=discord.Colour(3381759))
            await bot.say(embed=embed_msg)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


def load_credentials():
    with open('credentials.json') as f:
        return json.load(f)


if __name__ == '__main__':
    credentials = load_credentials()
    token = credentials['token']
    bot.run(token)