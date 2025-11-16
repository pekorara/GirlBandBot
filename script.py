import asyncio
import discord
from discord.ext import commands
import importlib
from utils.data_loader import load_mujica_list,load_mygo_list
from config import (
    TOKEN,
    MY_GUILD_ID,
    MYGO_BASE_URL,
    MUJICA_BASE_URL
)

# --- Bot 設定 ---
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

COG_MODULES = [
    "cogs.mygo",
    "cogs.mujica"
]

DEPS = {
    "mygo_base_url": MYGO_BASE_URL,
    'mujica_base_url': MUJICA_BASE_URL,
    "mygo_list": load_mygo_list(),
    "mujica_list": load_mujica_list(),
}

async def setup_cogs(bot: commands.Bot):
    for module_name in COG_MODULES:
        mod = importlib.import_module(module_name)
        setup = getattr(mod, "setup", None)
        if setup is None:
            raise RuntimeError(f"{module_name} 缺少 setup(bot, **deps)")
        await setup(bot, **DEPS)

@bot.event
async def on_ready():
    print(f"Bot : {bot.user}")
    try:
        guild = discord.Object(id=MY_GUILD_ID)
        bot.tree.copy_global_to(guild=guild)
        synced = await bot.tree.sync(guild=guild)

        print(f"成功同步 {len(synced)} 個指令")
        for cmd in synced:
            print(f"   /{cmd.name} - {cmd.description}")

    except Exception as e:
        print(f"同步失敗: {e}")

async def main():
    async with bot:
        await setup_cogs(bot)
        await bot.start(TOKEN)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("已中止")
