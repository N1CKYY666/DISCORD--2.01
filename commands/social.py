from pathlib import Path

import discord
from discord.ext import commands

GIF_PATH = (
    Path(__file__).resolve().parent.parent
    / "assets" / "gifs" / "divider1.gif"
)
FOOTER_TEXT = "THE REAL OLROX • Richter's childhood nightmare."


class Social(commands.Cog):
    """Handle member events and social interactions."""

    def __init__(self, bot):
        self.bot = bot

    def decorate_embed(self, embed):
        """Apply the standard Olrox divider and footer."""
        embed.set_image(url="attachment://divider1.gif")
        embed.set_footer(
            text=FOOTER_TEXT,
            icon_url=self.bot.user.display_avatar.url
        )
        return embed

    @staticmethod
    def divider_file():
        return discord.File(GIF_PATH, filename="divider1.gif")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Welcome new members to the server."""
        channel = discord.utils.get(
            member.guild.text_channels,
            name="bienvenidas"
        )

        if channel is None:
            return

        embed = discord.Embed(
            title="✦ ───────  AN ETERNAL WELCOME ─────── ✦",
            description=(
                "Oh? Another member has arrived.\n\n"
                f"Welcome to my domain, {member.mention}.\n"
                "Do try to keep up with the conversation."
            ),
            color=0x74459A
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        self.decorate_embed(embed)
        await channel.send(embed=embed, file=self.divider_file())

    @commands.command(name="testwelcome")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def test_welcome(self, ctx):
        """Test the welcome message without a new member."""
        await self.on_member_join(ctx.author)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Send a farewell message when a member leaves."""
        channel = discord.utils.get(
            member.guild.text_channels,
            name="despedidas"
        )

        if channel is None:
            return

        embed = discord.Embed(
            title="✦ ─────── A FAREWELL ─────── ✦",
            description=(
                "Oh? Someone has decided to leave the server.\n\n"
                f"Farewell, {member.display_name}.\n"
                "I suppose this place isn't for everyone.\n\n"
                "*What a pity.*"
            ),
            color=0x74459A
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        self.decorate_embed(embed)
        await channel.send(embed=embed, file=self.divider_file())

    @commands.command(name="testgoodbye")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def test_goodbye(self, ctx):
        """Test the farewell message without removing a member."""
        await self.on_member_remove(ctx.author)

    @commands.command(name="profile")
    @commands.guild_only()
    async def profile(self, ctx, member: discord.Member = None):
        """Display a server member's profile."""
        if member is None:
            member = ctx.author

        joined = (
            member.joined_at.strftime("%Y-%m-%d %H:%M:%S")
            if member.joined_at else "Unknown"
        )
        roles = ", ".join(
            role.name for role in member.roles if role.name != "@everyone"
        ) or "None"

        embed = discord.Embed(
            title="✦ ───── MEMBER PROFILE ───── ✦",
            description=(
                f"☾ **Name:** {member.display_name}\n"
                f"☾ **Joined:** {joined}\n"
                f"☾ **Created:** {member.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"☾ **Roles:** {roles}\n"
                f"☾ **Status:** {member.status}\n"
                f"☾ **Bot:** {'Yes' if member.bot else 'No'}"
            ),
            color=0x74459A
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        self.decorate_embed(embed)
        await ctx.send(embed=embed, file=self.divider_file())

    @commands.command(name="server")
    @commands.guild_only()
    async def server(self, ctx):
        """Display server information."""
        guild = ctx.guild
        owner = guild.owner.display_name if guild.owner else "Unknown"

        embed = discord.Embed(
            title="✦ ───── SERVER INFORMATION ───── ✦",
            description=(
                f"☾ **Name:** {guild.name}\n"
                f"☾ **Owner:** {owner}\n"
                f"☾ **Created:** {guild.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"☾ **Members:** {guild.member_count}\n"
                f"☾ **Roles:** {len(guild.roles)}\n"
            ),
            color=0x74459A
        )
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        self.decorate_embed(embed)
        await ctx.send(embed=embed, file=self.divider_file())


async def setup(bot):
    """Register the social Cog."""
    await bot.add_cog(Social(bot))
