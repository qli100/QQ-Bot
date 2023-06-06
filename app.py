# add bot link: 
# https://discord.com/api/oauth2/authorize?client_id=1080740415021514762&permissions=377957246976&scope=bot
import nextcord, requests, json, datetime, asyncio, os, openai
from nextcord import Embed
from nextcord.ext import commands
from urllib import response
from wsgiref import headers
from aiohttp import request
from dotenv import load_dotenv

intents = nextcord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command("help")

# get discord token and API keys
load_dotenv()
TOKEN = os.getenv("TOKEN")
KEY = os.getenv("KEY")
openai.api_key = KEY

# helper functions
async def delete(ctx):
    await asyncio.sleep(2)
    await ctx.message.delete()

# execute commands
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  
    if message.content.startswith("!chatgpt"):
        response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{message.content}",
        max_tokens=2048,
        temperature=0.5,
        )
        await message.channel.send(response.choices[0].text)
        return
    await bot.process_commands(message)

@bot.command(name="help")
async def Help(ctx):
    embed = Embed(color=0xedcc95, title="Commands")
    embed.add_field(name="!c, cor, corg, corgi", value="send a cute corgi picture", inline=False)
    embed.add_field(name="!a, af, aff, affirm, affirmation", value="send a positive affirmation", inline=False)
    embed.add_field(name="!j, jo, jok, joke, jokes", value="send a funny(?) joke", inline=False)
    embed.add_field(name="!hug", value="send a virtual hug", inline=False)
    embed.add_field(name="!chatgpt + text", value="ask chatgpt", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="corgi", aliases=["c", "cor", "corg"])
async def Corgi(ctx):
    response = requests.get("https://dog.ceo/api/breed/corgi/images/random")
    img = response.json()["message"]
    await ctx.send(img)
    await delete(ctx)

@bot.command(name="aff", aliases=["a", "af", "affirm", "affirmation"])
async def Affirmation(ctx):
    response = requests.get("https://www.affirmations.dev/")
    text = response.json()["affirmation"]
    embed = Embed(color=0xedcc95)
    embed.add_field(name=text, value='')
    await ctx.send(embed=embed)
    await delete(ctx)

@bot.command(name="joke", aliases=["j", "jo", "jok", "jokes"])
async def Joke(ctx):
    response = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})
    text = response.json()["joke"]
    embed = Embed(color=0xedcc95)
    embed.add_field(name=text, value='')
    await ctx.send(embed=embed)
    await delete(ctx)

@bot.command(name="hug")
async def Hug(ctx):
    await ctx.send("https://tenor.com/view/ghost-hug-you-cant-feel-it-but-its-there-gif-8158817")
    await delete(ctx)

@bot.event
async def on_ready():
    print(f"Running {bot.user.name}")

if __name__ == '__main__':
	bot.run(TOKEN)

