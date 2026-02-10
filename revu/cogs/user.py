from typing import List

import discord
from discord import app_commands
from discord.ext import commands
import selfcord

from gary.gary_self import get_gary
from utils import BaseGroupCog, is_authorized, log_command
from revu.utils.user_util import ProfileView


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(dms=True, guilds=True, private_channels=True)
class UserCog(BaseGroupCog, name="user"):
    """ """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__(bot)

    @app_commands.user_install()
    @app_commands.allowed_contexts(dms=True, guilds=True, private_channels=True)
    @app_commands.command(
        description="Get the avatar of a user in a specific size.", name="avatar"
    )
    @is_authorized()
    @log_command()
    async def avatar(
        self,
        interaction: discord.Interaction,
        size: str,
        user: discord.User | None = None,
    ) -> None:
        """ """

        target_user = user or interaction.user

        assert user
        avatar = user.avatar or user.default_avatar

        try:
            size_int = int(size)
            avatar_url = avatar.replace(format="png", size=size_int).url

            assert self.bot.user
            embed = discord.Embed(
                color=(
                    target_user.color.value if user.color else self.bot.user.color.value
                ),
                title=f"{target_user}'s avatar: {size}x{size}",
                url=avatar_url,
                timestamp=self.dates.date(),
            )

            embed.set_image(url=avatar_url)

            await interaction.response.send_message(embed=embed)

        except ValueError:
            await interaction.response.send_message(
                "Please provide a valid size: 2^x from 2 to 4096.", ephemeral=True
            )

    @app_commands.user_install()
    @app_commands.allowed_contexts(dms=True, guilds=True, private_channels=True)
    @app_commands.command(
        description="View account facts and information for a user.", name="profile"
    )
    @is_authorized()
    @log_command()
    async def profile(
        self,
        interaction: discord.Interaction,
        user: discord.User | None = None,
    ) -> None:
        """ """

        target_user = user or interaction.user

        try:
            embeds: List[discord.Embed] = []

            assert self.bot.user
            color_value = self.bot.user.color.value
            if hasattr(user, "color") and target_user.color.value != 0:
                color_value = target_user.color.value

            embed_main = discord.Embed(
                color=color_value,
                title=f"Profile: {target_user.name}",
                timestamp=self.dates.date(),
            )
            embed_main.set_thumbnail(url=target_user.display_avatar.url)

            created_at = discord.utils.format_dt(target_user.created_at, style="F")
            created_relative = discord.utils.format_dt(
                target_user.created_at, style="R"
            )

            embed_main.add_field(name="ID", value=f"`{target_user.id}`", inline=True)
            embed_main.add_field(
                name="Is Bot?", value="Yes" if target_user.bot else "No", inline=True
            )
            embed_main.add_field(
                name="Created Account",
                value=f"{created_at}\n({created_relative})",
                inline=False,
            )

            if target_user.public_flags:
                flags = [
                    name.replace("_", " ").title()
                    for name, value in target_user.public_flags
                    if value
                ]
                if flags:
                    embed_main.add_field(
                        name="Badges", value=", ".join(flags), inline=False
                    )

            embeds.append(embed_main)

            if interaction.guild and isinstance(user, discord.Member):
                embed_guild = discord.Embed(
                    color=color_value,
                    title=f"Server Details: {interaction.guild.name}",
                    timestamp=self.dates.date(),
                )
                embed_guild.set_thumbnail(url=user.display_avatar.url)

                if user.joined_at:
                    joined_at = discord.utils.format_dt(user.joined_at, style="F")
                    joined_relative = discord.utils.format_dt(user.joined_at, style="R")
                    embed_guild.add_field(
                        name="Joined Server",
                        value=f"{joined_at}\n({joined_relative})",
                        inline=False,
                    )

                try:
                    if user.top_role:
                        embed_guild.add_field(
                            name="Top Role", value=user.top_role.mention, inline=True
                        )
                except (TypeError, AttributeError):
                    pass

                embeds.append(embed_guild)

            embed_visuals = discord.Embed(
                color=color_value,
                title=f"{target_user.name}'s Visuals",
                description=f"[Avatar Link]({target_user.display_avatar.url})",
                timestamp=self.dates.date(),
            )
            embed_visuals.set_image(url=target_user.display_avatar.url)

            try:
                fetched_user = await self.bot.fetch_user(target_user.id)
                if fetched_user.banner:
                    embed_visuals.add_field(
                        name="Banner", value=f"[Banner Link]({fetched_user.banner.url})"
                    )
            except discord.HTTPException:
                pass

            embeds.append(embed_visuals)

            view = ProfileView(interaction, embeds)
            await interaction.response.send_message(embed=embeds[0], view=view)

        except Exception as e:
            self.log.error(f"Error in profile command: {e}")
            await interaction.response.send_message(
                "An unexpected error occurred while generating the profile.",
                ephemeral=True,
            )


# Adds the misc cog
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(UserCog(bot))
