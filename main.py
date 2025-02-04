# !/usr/bin/python 
# -*- coding: utf-8 -*- 

import discord
from discord.ext import commands
import json
import os
from dotenv import load_dotenv
from function import translate_text, get_language_lists, add_language, remove_language

# 讀取 .env 檔案
load_dotenv()

# 讀取設定檔
with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

# 設定 Intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=jdata['Prefix'], intents=intents, help_command=None)

# 初始狀態
auto_translate = True  # 是否自動翻譯

# 讀取 Token（避免公開 Token）
TOKEN = os.getenv("TOKEN")  # 或從設定檔讀取
if not TOKEN:
    raise ValueError("❌ 無法取得 Discord Bot Token，請檢查 .env 是否正確設定！")


@bot.event
async def on_ready():
    print(f'✅ 機器人已登入: {bot.user}')

@bot.event
async def on_message(msg):
    global auto_translate
    if msg.author.bot:
        return
    
    if msg.content.startswith(jdata['Prefix']):  # 忽略指令
        await bot.process_commands(msg)
        return

    if auto_translate and msg.content:
        result = translate_text(msg.content)
        # await msg.channel.send(result)

        embed = discord.Embed(description=result, color=0x3498db)  # 藍色
        embed.set_footer(text="🔄 自動翻譯")

        await msg.channel.send(embed=embed)

    

# 開啟/關閉翻譯功能
@bot.command()
async def toggle(ctx):
    global auto_translate
    auto_translate = not auto_translate
    status = "開啟" if auto_translate else "關閉"
    
    embed = discord.Embed(title="🔄 自動翻譯", description=f"自動翻譯功能已**{status}**！", color=0x2ecc71)
    await ctx.send(embed=embed)

# 新增翻譯語言
@bot.command()
async def add_lang(ctx, lang: str = None):
    if not lang:
        embed = discord.Embed(description="⚠️ 請輸入語言代碼，例如：`#add_lang fr`\n📌 使用 `#lang_list` 查看可用語言", color=0xf1c40f)
        await ctx.send(embed=embed)
        return

    result = add_language(lang)
    embed = discord.Embed(description=result, color=0x2ecc71)
    await ctx.send(embed=embed)

# 刪除翻譯語言
@bot.command()
async def remove_lang(ctx, lang: str = None):
    if not lang:
        embed = discord.Embed(description="⚠️ 請輸入語言代碼，例如：`#remove_lang es`\n📌 使用 `#lang_list` 查看可用語言", color=0xf1c40f)
        await ctx.send(embed=embed)
        return

    result = remove_language(lang)
    embed = discord.Embed(description=result, color=0xe74c3c)
    await ctx.send(embed=embed)

# 查看目前支援的語言清單
@bot.command()
async def lang_list(ctx):
    enabled, available = get_language_lists()
    
    enabled_text = "\n".join([f"✅ {name}" for _, name in enabled.items()])
    available_text = "\n".join([f"➕ {name}" for _, name in available.items()])

    embed = discord.Embed(title="🌍 翻譯語言列表", color=0x2ecc71)
    embed.add_field(name="✅ **目前支援的語言**", value=enabled_text, inline=False)
    embed.add_field(name="📌 **可以新增的語言**", value=available_text, inline=False)
    embed.set_footer(text="🔄 使用 #add_lang <語言代碼> 來新增語言")

    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    help_message = """**🤖 機器人指令列表：**
    
🔹 `/toggle` - **開啟/關閉** 自動翻譯功能
🔹 `/add_lang <語言代碼>` - **新增翻譯語言**（例如：`#add_lang fr`）
🔹 `/remove_lang <語言代碼>` - **刪除翻譯語言**（例如：`#remove_lang es`）
🔹 `/lang_list` - **查看目前支援的語言**（已啟用 & 可新增的）
🔹 `/say <文字>` - **讓機器人複誦文字**
🔹 `/help` - **顯示指令幫助**

📌 **支援的語言代碼範例：**
- `zh-TW`（繁體中文）
- `en`（English）
- `es`（Español）
- `ja`（日本語）
- 更多語言請使用 `/lang_list` 查看！

✨ **提示**：
- 輸入 `/toggle` 可**開啟/關閉** 自動翻譯功能。
- 若想新增語言，請先確認語言代碼是否正確。
    """
    await ctx.send(help_message)


# 測試指令
@bot.command()
async def say(ctx, *, text: str):
    embed = discord.Embed(description=text, color=0x95a5a6)
    await ctx.send(embed=embed)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    bot.run(TOKEN)
    