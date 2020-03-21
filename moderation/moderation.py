import discord
from discord.ext import commands
from datetime import datetime, timedelta
from core import checks
from core.models import PermissionLevel

class moderation(commands.Cog):
    """An easy way for your staff to moderate"""
    def __init__(self, bot):
        self.bot = bot
        self.errorcolor = 0xFF2B2B
        self.blurple = 0x7289DA


    
    #On channel create set up mute stuff
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        guild = channel.guild
        role = discord.utils.get(guild.roles, name = "Muted")
        if role == None:
            role = await guild.create_role(name = "Muted")
        await channel.set_permissions(role, send_messages = False)

    #Purge command
    @commands.command(aliases = ["clear"])
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def purge(self, ctx, amount = 10):
        """removes a set amount of messages in a channel"""
        max_purge = 2000
        if amount >= 1 and amount <= max_purge:
            await ctx.channel.purge(limit = amount + 1)
            embed = discord.Embed(
                title = "Purge",
                description = f"Purged {amount} message(s)!",
                color = self.blurple
            )
            await ctx.send(embed = embed, delete_after = 5.0)
            modlog = discord.utils.get(ctx.guild.text_channels, name = "modlogs")
            if modlog == None:
                return
            if modlog != None:
                embed = discord.Embed(
                    title = "Purge",
                    description = f"{amount} message(s) have been purged by {ctx.author.mention} in {ctx.message.channel.mention}",
                    color = self.blurple,
                    timestamp = datetime.utcnow()
                )
                await modlog.send(embed = embed)
        if amount < 1:
            embed = discord.Embed(
                title = "Purge Error",
                description = f"You must purge more then {amount} message(s)!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)
            await ctx.message.delete()
        if amount > max_purge:
            embed = discord.Embed(
                title = "Purge Error",
                description = f"You must purge less then {amount} messages!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)
            await ctx.message.delete()

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "You are missing the **Supporter** permission level!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)
            await ctx.message.delete()

    #Kick command
    @commands.command()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def kick(self, ctx, member : discord.Member = None, *, reason = None):
        """kicks a user from your server"""
        if member == None:
            embed = discord.Embed(
                title = "Kick Error",
                description = "Please specify a member!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)
        else:
            if member.id == ctx.message.author.id:
                embed = discord.Embed(
                    title = "Kick Error",
                    description = "You can't kick yourself!",
                    color = self.blurple
                )
                await ctx.send(embed = embed)
            else:
                if reason == None:
                    await member.kick(reason = f"Moderator - {ctx.message.author.name}#{ctx.message.author.discriminator}.\nReason - No reason proivded.")
                    embed = discord.Embed(
                        title = "Kick",
                        description = f"{member.mention} has been kicked by {ctx.message.author.mention}.",
                        color = self.blurple,
                        timestamp = datetime.utcnow()
                    )
                    await ctx.send(embed = embed)
                    modlog = discord.utils.get(ctx.guild.text_channels, name = "modlogs")
                    if modlog == None:
                        return
                    if modlog != None:
                        embed = discord.Embed(
                            title = "Kick",
                            description = f"{member.mention} has been kicked by {ctx.message.author.mention} in {ctx.message.channel.mention}.",
                            color = self.blurple,
                            timestamp = datetime.utcnow()
                        )
                        await modlog.send(embed = embed)
                else:
                    await member.kick(reason = f"Moderator - {ctx.message.author.name}#{ctx.message.author.discriminator}.\nReason - {reason}")
                    embed = discord.Embed(
                        title = "Kick",
                        description = f"{member.mention} has been kicked by {ctx.message.author.mention}\n\nReason: `{reason}`",
                        color = self.blurple,
                        timestamp = datetime.utcnow()
                    )
                    await ctx.send(embed = embed)
                    modlog = discord.utils.get(ctx.guild.text_channels, name = "modlogs")
                    if modlog == None:
                        return
                    if modlog != None:
                        embed = discord.Embed(
                            title = "Kick",
                            description = f"{member.mention} has been kicked by {ctx.message.author.mention} in {ctx.message.channel.mention}\n\nReason: `{reason}`",
                            color = self.blurple,
                            timestamp = datetime.utcnow()
                        )
                        await modlog.send(embed = embed)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "You are missing the **Moderator** permission level!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)

    #Ban command
    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def ban(self, ctx, member : discord.Member = None, *, reason = None):
        """bans a user from your server"""
        if member == None:
            embed = discord.Embed(
                title = "Ban Error",
                description = "Please specify a user!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)
        else:
            if member.id == ctx.message.author.id:
                embed = discord.Embed(
                    title = "Ban Error",
                    description = "Why are you trying to ban yourself...?\n\n You can't ban yourself!",
                    color = self.blurple
                )
                await ctx.send(embed = embed)
            else:
                if reason == None:
                    await member.ban(reason = f"Moderator - {ctx.message.author.name}#{ctx.message.author.discriminator}.\nReason - No Reason Provided.")
                    embed = discord.Embed(
                        title = "Ban",
                        description = f"{member.mention} has been banned by {ctx.message.author.mention}.",
                        color = self.blurple,
                        timestamp = datetime.utcnow()
                    )
                    modlog = discord.utils.get(ctx.guild.text_channels, name = "modlogs")
                    if modlog == None:
                        return
                    if modlog != None:
                        embed = discord.Embed(
                            title = "Ban",
                            description = f"{member.mention} has been banned by {ctx.message.author.mention}.",
                            color = self.blurple,
                            timestamp = datetime.utcnow()
                        )
                        await modlog.send(embed = embed)
                else:
                    await member.ban(reason = f"Moderator - {ctx.message.author.name}#{ctx.message.author.discriminator}.\nReason - {reason}")
                    embed = discord.Embed(
                        title = "Ban",
                        description = f"{member.mention} has been banned by {ctx.message.author.mention}\n\nReason: `{reason}`",
                        color = self.blurple,
                        timestamp = datetime.utcnow()
                    )
                    await ctx.send(embed = embed)
                    modlog = discord.utils.get(ctx.guild.text_channels, name = "modlogs")
                    if modlog == None:
                        return
                    if modlog != None:
                        embed = discord.Embed(
                            title = "Ban",
                            description = f"{member.mention} has been banned by {ctx.message.author.mention} in {ctx.message.channel.mention}\n\nReason: `{reason}`",
                            color = self.blurple,
                            timestamp = datetime.utcnow()
                        )
                        await modlog.send(embed = embed)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "You are missing the **Administrator** permission level!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)

    #Unban command
    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def unban(self, ctx, *, member : discord.User = None):
        """unbans a banned user"""
        if member == None:
            embed = discord.Embed(
                title = "Unban Error",
                description = "Please specify a user!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)
        else:
            banned_users = await ctx.guild.bans()
            for ban_entry in banned_users:
                user = ban_entry.user

                if (user.name, user.discriminator) == (member.name, member.discriminator):
                    embed = discord.Embed(
                        title = "Unban",
                        description = f"Unbanned {user.mention}",
                        color = self.blurple,
                        timestamp = datetime.utcnow()
                    )
                    await ctx.guild.unban(user)
                    await ctx.send(embed = embed)
                    modlog = discord.utils.get(ctx.guild.text_channels, name = "modlogs")
                    if modlog == None:
                        return
                    if modlog != None:
                        embed = discord.Embed(
                            title = "Ban",
                            description = f"{user.mention} has been unbanned by {ctx.message.author.mention} in {ctx.message.channel.mention}.",
                            color = self.blurple,
                            timestamp = datetime.utcnow()
                        )
                        await modlog.send(embed = embed)


    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "You are missing the **Administrator** permission level!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)

    #Mute command
    @commands.command()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def mute(self, ctx, member : discord.Member = None, *, reason = None):
        #"""mutes a user"""
        if member == None:
            embed = discord.Embed(
                title = "Mute Error",
                description = "Please specify a user!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)
        
        if ctx.message.author.top_role.position <= member.top_role.position:
            embed = discord.Embed(
                title = 'Mute Error',
                description = "You can't mute a person of a higher or equal rank.",
                color = self.errorcolor
            )
            return await ctx.send(embed = embed)
        else:
            if member.id == ctx.message.author.id:
                embed = discord.Embed(
                    title = "Mute Error",
                    description = "You can't mute yourself!",
                    color = self.errorcolor
                )
                await ctx.send(embed = embed, delete_after = 5.0)
            else:
                if reason == None:
                    role = discord.utils.get(ctx.guild.roles, name = "Muted")
                    staff = discord.utils.get(ctx.guild.roles, name = "Staff Muted")
                    support = discord.utils.get(ctx.guild.roles, name = "Support")
                    dev = discord.utils.get(ctx.guild.roles, name = "Developer")
                    devtemp = discord.utils.get(ctx.guild.roles, name="Dev")
                    # for channel in ctx.guild.text_channels:        #await ctx.send(channel.name)
                    #     await channel.set_permissions(staff, send_messages = False)
                    #     #await ctx.send("done_staff2")
                    #     await channel.set_permissions(role, send_messages = False)
                        #await ctx.send("done_role2")
                    if staff == None:
                        ctx.send('no staff muted role')
                    #ctx.se(f"Muted. {role.position}\nStaff. {staff.position}\nUser. {member.top_role.position}")
                    if member.top_role.position > role.position and member.top_role.position < staff.position:
                        await member.add_roles(staff)
                        await member.remove_roles(support)
                        #await ctx.send(member.top_role.name)
                        if dev in member.roles:
                            #await ctx.send("yes")
                            await member.remove_roles(dev)
                            await member.add_roles(devtemp)
                        #await ctx.send("staff")
                    if member.top_role.position < role.position:
                        await member.add_roles(role)
                        #await ctx.send("role")
                    
                    embed = discord.Embed(
                        title = "Mute",
                        description = f"{member.mention} has been muted by {ctx.message.author.mention} - `No reason provided`",
                        color = self.blurple,
                        timestamp = datetime.utcnow()
                    )
                    await ctx.send(embed = embed)
                    modlog = discord.utils.get(ctx.guild.text_channels, name = "modlogs")
                    if modlog == None:
                        return
                    if modlog != None:
                        embed = discord.Embed(
                            title = "Mute",
                            description = f"{member.mention} has been muted by {ctx.message.author.mention} in {ctx.message.channel.mention} - `No reason provided`",
                            color = self.blurple,
                            timestamp = datetime.utcnow()
                        )
                        await modlog.send(embed = embed)
                else:
                    role = discord.utils.get(ctx.guild.roles, name = "Muted")
                    staff = discord.utils.get(ctx.guild.roles, name = "Staff Muted")
                    support = discord.utils.get(ctx.guild.roles, name = "Support")
                    dev = discord.utils.get(ctx.guild.roles, name = "Developer")
                    devtemp = discord.utils.get(ctx.guild.roles, name="Dev")
                    # if role == None:
                    #     role = await ctx.guild.create_role(name = "Muted")
                    #     overwrite = discord.PermissionsOverwrite()
                        
                            
                    # for channel in ctx.guild.text_channels:        #await ctx.send(channel.name)
                    #     await channel.set_permissions(staff, send_messages = False)
                    #     #await ctx.send("done_staff2")
                    #     await channel.set_permissions(role, send_messages = False)
                    #     #await ctx.send("done_role2")
                    if staff == None:
                        ctx.send('no staff muted role again')
                    #ctx.send(f"Muted. {role.position}\nStaff. {staff.position}\nUser. {member.top_role.position}")
                    if member.top_role.position > role.position and member.top_role.position < staff.position:
                        await member.add_roles(staff)
                        await member.remove_roles(support)
                        #await ctx.send(member.top_role.name)
                        if dev in member.roles:
                            #await ctx.send("yes")
                            await member.remove_roles(dev)
                            await member.add_roles(devtemp)
                        #await ctx.send("staff2")
                    if member.top_role.position < role.position:
                        await member.add_roles(role)
                        #await ctx.send("role2")
                    
                    #await member.add_roles(role)
                    embed = discord.Embed(
                        title = "Mute",
                        description = f"{member.mention} has been muted by {ctx.message.author.mention}\n\nReason: `{reason}`",
                        color = self.blurple,
                        timestamp = datetime.utcnow()
                    )
                    await ctx.send(embed = embed)
                    modlog = discord.utils.get(ctx.guild.text_channels, name = "modlogs")
                    if modlog == None:
                        return
                    if modlog != None:
                        embed = discord.Embed(
                            title = "Mute",
                            description = f"{member.mention} has been muted by {ctx.message.author.mention} in {ctx.message.channel.mention}\n\nReason: `{reason}`",
                            color = self.blurple,
                            timestamp = datetime.utcnow()
                        )
                        await modlog.send(embed = embed)

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions!",
                description = "You are missing the **Moderator** permission level!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)

     #Unmute command
    @commands.command()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def unmute(self, ctx, member : discord.Member = None, *, reason = None):
        """unmutes a user that was muted"""
        if member == None:
            embed = discord.Embed(
                title = "Unmute Error",
                description = "Please specify a user!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)
        else:
            if reason == None:
                role = discord.utils.get(ctx.guild.roles, name = "Muted")
                staff = discord.utils.get(ctx.guild.roles, name = "Staff Muted")
                support = discord.utils.get(ctx.guild.roles, name = "Support")
                dev = discord.utils.get(ctx.guild.roles, name = "Developer")
                devtemp = discord.utils.get(ctx.guild.roles, name="Dev")
                if role in member.roles:
                    await member.remove_roles(role)
                    embed = discord.Embed(
                        title = "Unmute",
                        description = f"{member.mention} has been unmuted by {ctx.message.author.mention}.",
                        color = self.blurple,
                        timestamp = datetime.utcnow()
                    )
                    await ctx.send(embed = embed)
                    modlog = discord.utils.get(ctx.guild.text_channels, name = "modmodlogs")
                    if modlog == None:
                        return
                    if modlog != None:
                        embed = discord.Embed(
                            title = "Unmute",
                            description = f"{member.mention} has been unmuted by {ctx.message.author.mention} in {ctx.message.channel.mention} - `No reason provided`",
                            color = self.blurple,
                            timestamp = datetime.utcnow()
                        )
                        await modlog.send(embed = embed)
                elif staff in member.roles:
                    await member.remove_roles(staff)
                    await member.add_roles(support)
                    if devtemp in member.roles:
                        await member.add_roles(dev)
                        await member.remove_roles(devtemp)
                    embed = discord.Embed(
                        title = "Unmute",
                        description = f"{member.mention} has been unmuted by {ctx.message.author.mention} - `No reason provided`",
                        color = self.blurple,
                        timestamp = datetime.utcnow()
                    )
                    await ctx.send(embed = embed)
                    modlog = discord.utils.get(ctx.guild.text_channels, name = "modlogs")
                    if modlog == None:
                        return
                    if modlog != None:
                        embed = discord.Embed(
                            title = "Unmute",
                            description = f"{member.mention} has been unmuted by {ctx.message.author.mention} in {ctx.message.channel.mention} - `No reason provided`",
                            color = self.blurple,
                            timestamp = datetime.utcnow()
                        )
                        await modlog.send(embed = embed)    
                else:
                    embed = discord.Embed(
                        title = "Unmute Error",
                        description = f"{member.mention} is not muted!",
                        color = self.errorcolor
                    )
                    await ctx.send(embed = embed)
            else:
                role = discord.utils.get(ctx.guild.roles, name = "Muted")
                staff = discord.utils.get(ctx.guild.roles, name = "Staff Muted")
                support = discord.utils.get(ctx.guild.roles, name = "Support")
                dev = discord.utils.get(ctx.guild.roles, name = "Developer")
                devtemp = discord.utils.get(ctx.guild.roles, name="Dev")
                if role in member.roles:
                    await member.remove_roles(role)
                    embed = discord.Embed(
                        title = "Unmute",
                        description = f"{member.mention} has been unmuted by {ctx.message.author.mention}.",
                        color = self.blurple,
                        timestamp = datetime.utcnow()
                    )
                    await ctx.send(embed = embed)
                    modlog = discord.utils.get(ctx.guild.text_channels, name = "modlogs")
                    if modlog == None:
                        return
                    if modlog != None:
                        embed = discord.Embed(
                            title = "Unmute",
                            description = f"{member.mention} has been unmuted by {ctx.message.author.mention} in {ctx.message.channel.mention}\n\nReason: `{reason}`",
                            color = self.blurple,
                            timestamp = datetime.utcnow()
                        )
                        await modlog.send(embed = embed)
                elif staff in member.roles:
                    await member.remove_roles(staff)
                    await member.add_roles(support)
                    if devtemp in member.roles:
                        await member.add_roles(dev)
                        await member.remove_roles(devtemp)
                    embed = discord.Embed(
                        title = "Unmute",
                        description = f"{member.mention} has been unmuted by {ctx.message.author.mention}\n\nReason: `{reason}`",
                        color = self.blurple,
                        timestamp = datetime.utcnow()
                    )
                    await ctx.send(embed = embed)
                    modlog = discord.utils.get(ctx.guild.text_channels, name = "modlogs")
                    if modlog == None:
                        return
                    if modlog != None:
                        embed = discord.Embed(
                            title = "Unmute",
                            description = f"{member.mention} has been unmuted by {ctx.message.author.mention} in {ctx.message.channel.mention}\n\nReason: `{reason}`",
                            color = self.blurple,
                            timestamp = datetime.utcnow()
                        )
                        await modlog.send(embed = embed)    
                else:
                    embed = discord.Embed(
                        title = "Unmute Error",
                        description = f"{member.mention} is not muted!",
                        color = self.errorcolor
                    )
                    await ctx.send(embed = embed)
            

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions!",
                description = "You are missing the **Moderator** permission level!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)

    #Softban
    @commands.command(aliases = ["lightban"])
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def softban(self, ctx, member : discord.Member = None, *, reason = None):
        """bans a user and then unbans them, simple really"""
        if member == None:
            embed = discord.Embed(
                title = "Softban Error",
                description = "Please specify a user!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)
        else:
            if member.id == ctx.message.author.id:
                embed = discord.Embed(
                    title = "Softban Error",
                    description = "You can't softban yourself!",
                    color = self.blurple
                )
                await ctx.send(embed = embed)
            else:
                if reason == None:
                    await member.ban(reason = f"Softban by {ctx.message.author.name}#{ctx.message.author.discriminator}.\nReason - No Reason Provided.")
                    await member.unban()
                    embed = discord.Embed(
                        title = "Softban",
                        description = f"{member.mention} has been softbanned by {ctx.message.author.mention}",
                        color = self.blurple,
                        timestamp = datetime.utcnow()
                    )
                    await ctx.send(embed = embed)
                    modlog = discord.utils.get(ctx.guild.text_channels, name = "modlogs")
                    if modlog == None:
                        return
                    if modlog != None:
                        embed = discord.Embed(
                            title = "Softban",
                            description = f"{member.mention} has been softbanned by {ctx.message.author.mention}.",
                            color = self.blurple,
                            timestamp = datetime.utcnow()
                        )
                        await modlog.send(embed = embed)
                else:
                    await member.ban(reason = f"Softban by {ctx.message.author.name}#{ctx.message.author.discriminator}.\nReason - {reason}.")
                    await member.unban()
                    embed = discord.Embed(
                        title = "Softban",
                        description = f"{member.mention} has been softbanned by {ctx.message.author.mention}\n\nReason: `{reason}`.",
                        color = self.blurple,
                        timestamp = datetime.utcnow()
                    )
                    await ctx.send(embed = embed)
                    modlog = discord.utils.get(ctx.guild.text_channels, name = "modlogs")
                    if modlog == None:
                        return
                    if modlog != None:
                        embed = discord.Embed(
                            title = "Softban",
                            description = f"{member.mention} has been softbanned by {ctx.message.author.mention}\n\nReason: `{reason}`.",
                            color = self.blurple,
                            timestamp = datetime.utcnow()
                        )
                        embed.set_thumbnail(
                    url= ctx.message.author.avatar_url
                    )
                        await modlog.send(embed = embed)

    @softban.error
    async def softban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions!",
                description = "You are missing the **Administrator** permission level!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)

    #Nuke command
    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def nuke(self, ctx, *, reason):
        """clears a whole channel of its chat, non reversible and can destroy a server"""
        await ctx.send(
            embed=await self.generate_embed("Are you sure you want to nuke the channel? **This cannot be undone!** `[y/n]`")
        )

        def check(msg: discord.Message):
            return ctx.author == msg.author and ctx.channel == msg.channel

        embed_res: discord.Message = await self.bot.wait_for("message", check=check)
        # await ctx.send(embed_res.content)
        if embed_res.content.lower() == 'n':
            embed = discord.Embed(
                    title = "Nuke",
                    description = "Nuke has been cancelled.",
                    color = self.blurple
                )
            await ctx.send(embed = embed)
            return
        elif embed_res.content != 'cancel' and embed_res.content.lower() == 'y':

            channel_position = ctx.channel.position
            new_channel = await ctx.channel.clone()
            #await ctx.channel.send(reason)
            await new_channel.edit(position = channel_position, reason= f"Nuke - {ctx.message.author.name}#{ctx.message.author.discriminator}.\nReason - {reason}")
            await ctx.channel.delete(reason= f"Nuked - {ctx.message.author.name}#{ctx.message.author.discriminator}.\nReason - {reason}" )
            embed = discord.Embed(
                title = "Nuke",
                description  = "**The Earth God Waffle has spoken.**\n\nThis channel was nuked!.",
                color = self.blurple
            )
            #embed.set_image(url = "https://cdn.discordapp.com/attachments/600843048724987925/600843407228928011/tenor.gif")
            embed.set_image(url = "https://media2.giphy.com/media/cRBRQf8syLUyY/giphy.gif")
            await new_channel.send(embed = embed, delete_after = 60.0)
            modlog = discord.utils.get(ctx.guild.text_channels, name = "modlogs")
            if modlog == None:
                pass
            if modlog != None:
                embed = discord.Embed(
                    title = "Nuke",
                    description = f"{ctx.message.author.mention} has nuked {new_channel.mention}\n\nwith the reason: `{reason}`.",
                    color = self.blurple,
                    timestamp = datetime.utcnow() 
                )
                embed.set_thumbnail(
                    url= ctx.message.author.avatar_url
                    )
                await modlog.send(embed = embed)

    @nuke.error
    async def nuke_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions!",
                description = "You are missing the **Administator** permission level!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)


    @staticmethod
    async def generate_embed(description: str):
        embed = discord.Embed()
        embed.colour = discord.Colour.blurple()
        embed.description = description

        return embed


    

        # def check_reaction(reaction: discord.Reaction, user: discord.Member):
        #     return ctx.author == user and (str(reaction.emoji == "✅") or str(reaction.emoji) == "❌")

    

def setup(bot):
    bot.add_cog(moderation(bot))
