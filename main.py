import discord
from discord.ext import commands
from deep_translator import GoogleTranslator
import json

with open('setting.json', 'r', encoding= 'utf8') as jfile:
	jdata = json.load(jfile)

intents = discord.Intents.default()
intents.message_content = True  # 啟用訊息內容權限
bot = commands.Bot(command_prefix = jdata['Prefix'], intents = intents)

def translate_text(text):
    try:
        translated_zh = GoogleTranslator(source='auto', target='zh-TW').translate(text)
        translated_en = GoogleTranslator(source='auto', target='en').translate(text)
        translated_es = GoogleTranslator(source='auto', target='es').translate(text)
        translated_ja = GoogleTranslator(source='auto', target='ja').translate(text)  # 新增日文翻譯
        
        return f"**中文:** \t\t{translated_zh}\n**English:**    {translated_en}\n**Español:**   {translated_es}\n**日本語:** \t{translated_ja}"
    except Exception as e:
        return f"Error: {str(e)}"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(msg):
    if msg.author.id != 1335988945951002684 and len(msg.content) > 0 and msg.stickers == None:
        result = translate_text(msg.content)
        await msg.channel.send(result)

# @bot.command()
# async def trans(ctx, *, text: str):
#     result = translate_text(text)
#     await ctx.send(result)

@bot.command()
async def say(ctx, *, text: str):
    await ctx.send(text)

TOKEN = "MTMzNTk4ODk0NTk1MTAwMjY4NA.GqDzOq.S6kRRI2bTTwPkyFDapq3NOC3DN-YBU3adqCSzQ"
if __name__ == "__main__":
    bot.run(TOKEN)
