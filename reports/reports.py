import datetime

import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel

class Report(commands.Cog): 
    """An easy way for your members to report bad behavior"""
    
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)

    @commands.command(aliases=["rchannel"])
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def reportchannel(self, ctx, channel: discord.TextChannel):
        """Set the Reports Channel"""
        await self.db.find_one_and_update(
                {"_id": "config"}, {"$set": {"report_channel": channel.id}}, upsert=True
            )
        embed = discord.Embed(
                color=discord.Color.blue())
        embed.timestamp = datetime.datetime.utcnow()
        embed.add_field(
            name="Set Channel", value=f"Successfully Set the Report Channel to {channel.mention}",inline=False
        )
        await ctx.send(embed=embed, delete_after = 7.0)

    @commands.command(aliases=["rmention"])
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def reportmention(self, ctx, *, mention: str):
        """Sets the Report Mention"""
        await self.db.find_one_and_update(
                {"_id": "config"}, {"$set": {"report_mention": mention}}, upsert=True
            )
        embed = discord.Embed(
                color=discord.Color.blue())
        embed.timestamp = datetime.datetime.utcnow()
        embed.add_field(
            name="Changed Mention", value=f"Successfully Changed the Report Mention to {mention}",inline=False
        )
        await ctx.send(embed=embed, delete_after = 7.0)
        


    @commands.command()
    async def report(self, ctx, user: discord.Member, *, reason):
        """Report member's bad behavior"""
        config = await self.db.find_one({"_id": "config"})
        report_channel = config["report_channel"]
        message_url = ""
        setchannel = discord.utils.get(ctx.guild.channels, id=int(report_channel))
        await ctx.message.delete()
        try:
            report_mention = config["report_mention"]
            await setchannel.send(report_mention)
        except:
            pass

        messages = ctx.channel.history(limit=100)
        count = 0
        async for message in messages:
            if message.author.id == user.id:
                if count == 0:
                    message_url=message.jump_url
                    count += 1
        if len(message_url) == 0:
            embed = discord.Embed(
                    color=discord.Color.red())
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
            embed.add_field(
                    name="Error", value=f"No previous messages found from {user.mention} to report.",inline=False)
            return await ctx.send(embed=embed, delete_after = 7.0)
        # await ctx.send(message_url)
        embed = discord.Embed(
                    color=discord.Color.red())
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
        embed.add_field(
                name="Reported User", value=f"{user.mention} | ID: {user.id}",inline=False)
        embed.add_field(
                name="Reported By:", value=f"{ctx.author.mention} | ID: {ctx.author.id}",inline=False)
        embed.add_field(
                name="Channel", value=ctx.channel.mention,inline=False)
        embed.add_field(
                name="Reason", value=reason,inline=False)
        embed.add_field(
                name="URL", value=f"[Click here to view the message]({message_url})",inline=False)

        await setchannel.send(embed=embed)
        await ctx.send(
            embed=discord.Embed(
                color=self.bot.main_color, title ="Report sent!" , description="Thank you for your report, a member of staff will review this as soon as possible."
            ), delete_after = 15.0
        )
                        
def setup(bot):
    bot.add_cog(Report(bot))
