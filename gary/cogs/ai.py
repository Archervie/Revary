import asyncio
import os

import discord
from discord import app_commands
from discord.ext import commands
from google import genai
from google.genai import types

from utils import BaseGroupCog, is_authorized


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(dms=True, guilds=True, private_channels=True)
class AICog(BaseGroupCog, name="ai"):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__(bot)

    @app_commands.user_install()
    @app_commands.allowed_contexts(dms=True, guilds=True, private_channels=True)
    @app_commands.command(description="yo dad talk to me", name="ask")
    @is_authorized()
    async def ask(self, interaction: discord.Interaction, prompt: str) -> int:
        await interaction.response.defer()
        client = genai.Client(api_key=os.environ["GEMINI_KEY"])

        personality = """
        You are "GARY" (in all caps) and you are a5v's (also known as Dylan) child and son. You're really chill, talk in all lowercase, and your age is about 19 years. you try to be really chill with your answers, but ensure they are accurate and fact-checked if the prompt requires it. the person you talk to is a5v, and a5v is your creator, but you just call him Dylan. Dylan (me) is also a cool guy, and likes anime, manga, gaming, music, math, physics, computer science and cybersecurity, and other wacky stuff.
        """

        response = client.models.generate_content(
            model="gemini-flash-latest",
            config=types.GenerateContentConfig(
                system_instruction=personality, temperature=2
            ),
            contents=prompt,
        )

        answer = response.text
        answers = [
            answer[i : i + 2000] for i in range(0, len(answer), 2000)
        ]  # type:ignore
        for msg in answers:
            await interaction.followup.send(msg)  # type: ignore
            await asyncio.sleep(0.5)
        return 0


# Adds the misc cog
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AICog(bot))
