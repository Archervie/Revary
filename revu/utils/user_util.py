import discord
from typing import List


class ProfileView(discord.ui.View):
    def __init__(
        self,
        interaction: discord.Interaction,
        embeds: List[discord.Embed],
        timeout: float = 180.0,
    ):
        super().__init__(timeout=timeout)
        self.interaction = interaction
        self.embeds = embeds
        self.current_page = 0
        self.update_buttons()

    def update_buttons(self) -> None:
        """Updates the state of the buttons based on the current page."""
        self.previous.disabled = self.current_page == 0
        self.next.disabled = self.current_page == len(self.embeds) - 1

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Ensures only the command invoker can use the buttons."""
        if interaction.user.id != self.interaction.user.id:
            await interaction.response.send_message(
                "You cannot interact with this menu.", ephemeral=True
            )
            return False
        return True

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary)
    async def previous(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        self.current_page -= 1
        self.update_buttons()
        await interaction.response.edit_message(
            embed=self.embeds[self.current_page], view=self
        )

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        self.current_page += 1
        self.update_buttons()
        await interaction.response.edit_message(
            embed=self.embeds[self.current_page], view=self
        )
