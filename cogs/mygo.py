import typing
from urllib.parse import quote
import discord
from discord import app_commands
from discord.ext import commands
from utils.text_utils import normalize_text

class Mygo(commands.Cog):
    def __init__(self, bot : commands.Bot,mygo_url : str,mygo__list : list[dict]):
        self.bot = bot
        self.mygo_url = mygo_url
        self.mygo_list = mygo__list

    async def mygo_autocompleter(
            self,
            interaction: discord.Interaction,
            current: str
    ) -> typing.List[app_commands.Choice[str]]:
        choices = []
        norm_current = normalize_text(current)
        for item in self.mygo_list:
            alt = item.get("alt", "")
            if norm_current in alt:
                choices.append(app_commands.Choice(name=alt, value=alt))
        return choices[:25]

    @app_commands.command(name="mygo", description="顯示 MyGO 的台詞")
    @app_commands.describe(text="需要尋找的台詞")
    @app_commands.autocomplete(text=mygo_autocompleter)
    async def mygo(self,interaction: discord.Interaction, text: str):
        try:
            encoded_text = quote(text, safe='')
            image_url = f"{self.mygo_url}{encoded_text}.jpg"

            embed = discord.Embed(
                title=f"{text}",
                color=discord.Color.blue()
            )
            embed.set_image(url=image_url)

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await interaction.response.send_message(f"發生錯誤: {str(e)}", ephemeral=True)

async def setup(bot: commands.Bot, **deps):
    await bot.add_cog(Mygo(bot, deps.get("mygo_base_url"), deps.get("mygo_list")))