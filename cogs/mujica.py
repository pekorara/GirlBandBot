import typing
from urllib.parse import quote
import discord
from discord import app_commands
from discord.ext import commands
from utils.text_utils import normalize_text


class Mujica(commands.Cog):
    def __init__(self, bot,mujica_base_url : str, mujica_list : list[dict]):
        self.bot = bot
        self.mujica_base_url = mujica_base_url
        self.mujica_list = mujica_list

    async def mujica_autocompleter(
            self,
            interaction: discord.Interaction,
            current: str
    ) -> typing.List[app_commands.Choice[str]]:
        choices = []
        norm_current = normalize_text(current)
        print(norm_current)
        for item in self.mujica_list:
            alt = item.get("alt","")
            if norm_current in alt:
                choices.append(app_commands.Choice(name=alt, value=alt))
        return choices[:25]

    @app_commands.command(name="mujica", description="顯示 Mujica 的圖片")
    @app_commands.describe(text="需要尋找的圖片名稱")
    @app_commands.autocomplete(text=mujica_autocompleter)
    async def mujica(self,interaction: discord.Interaction, text: str):
        try:
            found_item = None
            for item in self.mujica_list:
                alt_value = item.get("alt","")
                if alt_value == text:
                    found_item = item
                    break

            if not found_item:
                error_msg = f"❌ 找不到名稱為 `{text}` 的圖片\n"
                await interaction.response.send_message(error_msg, ephemeral=True)
                return

            file_id = found_item.get("id", "")
            image_url = f"{self.mujica_base_url}{file_id}"

            embed = discord.Embed(
                title=f"{text}",
                color=discord.Color.purple()
            )
            embed.set_image(url=image_url)

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await interaction.response.send_message(f"❌ 發生錯誤: {str(e)}\n", ephemeral=True)

async def setup(bot: commands.Bot,**deps):
    await bot.add_cog(Mujica(bot,deps.get("mujica_base_url"),deps.get("mujica_list")))
