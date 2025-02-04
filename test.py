import discord
from discord.ext import commands
import json
import os
from function import translate_text, get_language_lists, add_language, remove_language

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
TOKEN = jdata["Token"]  # 或從設定檔讀取

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

    await bot.process_commands(msg)  # 確保指令仍可運行

# 開啟/關閉翻譯功能
@bot.command()
async def toggle(ctx):
    global auto_translate
    auto_translate = not auto_translate
    status = "開啟" if auto_translate else "關閉"
    await ctx.send(f"🔄 自動翻譯功能已{status}！")

# 新增翻譯語言
@bot.command()
async def add_lang(ctx, lang: str = None):
    if not lang:  # 如果 lang 為 None（使用者沒有輸入語言）
        await ctx.send("⚠️ 請輸入語言代碼，例如：`#add_lang fr`")
        return

    result = add_language(lang)
    await ctx.send(result)

@bot.command()
async def remove_lang(ctx, lang: str = None):
    if not lang:  # 如果 lang 為 None（使用者沒有輸入語言）
        await ctx.send("⚠️ 請輸入語言代碼，例如：`#remove_lang es`")
        return

    result = remove_language(lang)
    await ctx.send(result)

# 查看目前支援的語言清單
@bot.command()
async def lang_list(ctx):
    enabled, available = get_language_lists()
    
    enabled_text = "\n".join([f"✅ {code} {name}" for code, name in enabled.items()])
    available_text = "\n".join([f"➕ {code} {name}" for code, name in available.items()])

    message = f"🌍 **目前支援的翻譯語言：**\n{enabled_text}\n\n📌 **可以新增的語言：**\n{available_text}"
    await ctx.send(message)

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
    await ctx.send(text)

if __name__ == "__main__":
    bot.run(TOKEN)