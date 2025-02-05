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
auto_translate_global = True  # 預設為開啟
no_translate_channels = set()

# 讀取 Token（避免公開 Token）
TOKEN = os.getenv("TOKEN")  # 或從設定檔讀取
if not TOKEN:
    raise ValueError("❌ 無法取得 Discord Bot Token，請檢查 .env 是否正確設定！")


@bot.event
async def on_ready():
    print(f'✅ 機器人已登入: {bot.user}')

@bot.event
async def on_message(msg):
    if msg.author.bot:
        return

    # 確保指令仍可運行
    if msg.content.startswith(jdata['Prefix']):
        await bot.process_commands(msg)
        return

    # 檢查是否在「不要翻譯的頻道」
    if auto_translate_global and msg.channel.id not in no_translate_channels:
        result = translate_text(msg.content)
        if isinstance(result, discord.Embed):
            await msg.channel.send(embed=result)  # 直接發送 Embed
        else:
            await msg.channel.send(result)  # 發送錯誤訊息

    

# 開啟/關閉翻譯功能
# @bot.command()
# async def toggle(ctx):
#     global auto_translate
#     auto_translate = not auto_translate
#     status = "開啟" if auto_translate else "關閉"
    
#     embed = discord.Embed(title="🔄 自動翻譯", description=f"自動翻譯功能已**{status}**！", color=0x2ecc71)
#     await ctx.send(embed=embed)

@bot.command()
async def toggle_all(ctx):
    """ 開啟/關閉全伺服器的翻譯 """
    global auto_translate_global
    auto_translate_global = not auto_translate_global
    status = "開啟" if auto_translate_global else "關閉"
    status_en = "Enabled" if auto_translate_global else "Disabled"
    
    embed = discord.Embed(title="🔄 全伺服器翻譯 | Server-wide Translation",description=f"全伺服器翻譯已**{status}**！\nServer-wide translation is now **{status_en}**!",color=0x2ecc71 if auto_translate_global else 0xe74c3c)
    await ctx.send(embed=embed)

@bot.command()
async def toggle_channel(ctx):
    """ 開啟/關閉目前頻道的翻譯 """
    channel_id = ctx.channel.id
    if channel_id in no_translate_channels:
        no_translate_channels.remove(channel_id)  # 從禁止清單移除，代表開啟翻譯
        status_zh = "開啟"
        status_en = "Enabled"
    else:
        no_translate_channels.add(channel_id)  # 加入禁止清單，代表關閉翻譯
        status_zh = "關閉"
        status_en = "Disabled"

    embed = discord.Embed(title="🔄 頻道翻譯 | Channel Translation",description=f"本頻道翻譯已**{status_zh}**！\nTranslation in this channel is now **{status_en}**!",color=0x2ecc71 if status_zh == "開啟" else 0xe74c3c)
    await ctx.send(embed=embed)

# 新增翻譯語言
@bot.command()
async def add_lang(ctx, lang: str = None):
    if not lang:
        embed = discord.Embed(description="⚠️ 請輸入語言代碼，例如：`#add_lang fr`\n📌 使用 `#lang_list` 查看可用語言。\n""⚠️ Please enter a language code, e.g., `#add_lang fr`\n📌 Use `#lang_list` to see available languages.",color=0xf1c40f)  
        await ctx.send(embed=embed)
        return

    result = add_language(lang)
    result_en = f"✅ Language **{lang}** has been added!" if "已新增" in result else f"⚠️ Language **{lang}** already exists or is not supported!"
    
    embed = discord.Embed(description=f"{result}\n{result_en}", color=0x2ecc71)
    await ctx.send(embed=embed)

# 刪除翻譯語言
@bot.command()
async def remove_lang(ctx, lang: str = None):
    """ 移除翻譯語言 """
    if not lang:
        embed = discord.Embed(
            description="⚠️ 請輸入語言代碼，例如：`#remove_lang es`\n📌 使用 `#lang_list` 查看可用語言。\n"
                        "⚠️ Please enter a language code, e.g., `#remove_lang es`\n📌 Use `#lang_list` to see available languages.",
            color=0xf1c40f
        )
        await ctx.send(embed=embed)
        return

    result = remove_language(lang)
    result_en = f"❌ Language **{lang}** has been removed!" if "已移除" in result else f"⚠️ Language **{lang}** does not exist in the current list!"

    embed = discord.Embed(description=f"{result}\n{result_en}", color=0xe74c3c)
    await ctx.send(embed=embed)

# 查看目前支援的語言清單
@bot.command()
async def lang_list(ctx):
    """ 查看目前支援的語言 """
    enabled, available = get_language_lists()
    
    enabled_text = "\n".join([f"✅ {name} ({code})" for code, name in enabled.items()])
    available_text = "\n".join([f"➕ {name} ({code})" for code, name in available.items()])

    embed = discord.Embed(title="🌍 翻譯語言列表 | Supported Languages", color=0x2ecc71)
    embed.add_field(name="✅ **目前支援的語言 | Enabled Languages**", value=enabled_text if enabled_text else "無 | None", inline=False)
    embed.add_field(name="📌 **可以新增的語言 | Available to Add**", value=available_text if available_text else "無 | None", inline=False)

    await ctx.send(embed=embed)




@bot.command()
async def help(ctx):
    """ 顯示幫助指令 """
    embed = discord.Embed(title="🤖 機器人指令列表 | Bot Commands", color=0x3498db)
    
    embed.add_field(
        name="🔄 翻譯功能 | Translation Controls",
        value="    `/toggle_all` - **開啟/關閉** 整個伺服器的翻譯\n"
              "    `/toggle_channel` - **開啟/關閉** 目前頻道的翻譯\n"
              "    `/lang_list` - **查看目前支援的語言**\n\n"
              "    `/toggle_all` - **Enable/Disable** server-wide translation\n"
              "    `/toggle_channel` - **Enable/Disable** translation in this channel\n"
              "    `/lang_list` - **View currently supported languages**",
        inline=False
    )

    embed.add_field(
        name="\n🌍 語言管理 | Language Management",
        value="    `/add_lang <語言代碼>` - **新增翻譯語言**\n"
              "    `/remove_lang <語言代碼>` - **刪除翻譯語言**\n\n"
              "    `/add_lang <language code>` - **Add a translation language**\n"
              "    `/remove_lang <language code>` - **Remove a translation language**",
        inline=False
    )

    embed.add_field(
        name="\n💬 其他指令 | Other Commands",
        value="    `/say <文字>` - **讓機器人複誦文字**\n"
              "    `/help` - **顯示指令幫助**\n\n"
              "    `/say <text>` - **Make the bot repeat a message**\n"
              "    `/help` - **Show command help**",
        inline=False
    )


    await ctx.send(embed=embed)


# 測試指令
@bot.command()
async def say(ctx, *, text: str):
    embed = discord.Embed(description=text, color=0x95a5a6)
    await ctx.send(embed=embed)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    bot.run(TOKEN)
    