import discord
from discord.ext import commands
import pickle
"""
This bots purpose is to notify admins/mods when a user banned in a different server joins.
listened servers are servers that the bot is allowed to check for banned users.
subscribers are users that recieve notifications when a user banned in a specific listened server joins a specific server.

listeners are stored as ids in a list.
subscribers are stored as dicts in a list.

subscribers have the following keys:
    server1: server id
    server2: server id
    user: user id


commands:

listen:
    description:
        add a server to a list of servers to allow notifications
    aliases:
        add
    examples:
        b!listen 123456789012345678
    permissions:
        admininstrator
        
unlisten:
    parameters:
        server
    description:
        stop listening to a server
    aliases:
        remove
    permissions:
        admininstrator

subscribe:
    parameters:
        server: server id (the id of the server to subscribe to)
        user: user id (the id of the user that is subscribing, this allows admins to subscribe other users)
    description:
        start notifying that user when a user banned in "server" joins the server the command is used in
    aliases:
        sub
    examples:
        b!sub 123456789012345678 @user 123456789012345678
    permissions:
        admininstrator

unsubscribe:
    parameters:
        server
        user
    description:
        removes a subscription to a user, no further explanation needed
    aliases:
        unsub
    permissions:
        admininstrator
"""
class commands(commands.Cog):
    # make bot accessible to the rest of the class
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=['add'])
    async def listen(self, ctx):
        bot = self.bot
        if ctx.author.guild_permissions.administrator:
            server = ctx.guild.id
            if server not in bot.listeners_:
                bot.listeners_.append(server)
                with open('/saves/bannotif/listeners.p', 'wb') as f:
                    pickle.dump(bot.listeners_, f)
                await ctx.send(f'{ctx.author.mention} added server {server} to the list of servers to listen to.')
            else:
                await ctx.send(f'{ctx.author.mention} server {server} is already being listened to.')
        else:
            await ctx.send(f'{ctx.author.mention} you do not have permission to use this command.')

    @commands.command(aliases=['remove'])
    async def unlisten(self, ctx):
        bot = self.bot
        if ctx.author.guild_permissions.administrator:
            server = ctx.guild.id
            if server in bot.listeners_:
                bot.listeners_.remove(server)
                with open('/saves/bannotif/listeners.p', 'wb') as f:
                    pickle.dump(bot.listeners_, f)
                await ctx.send(f'{ctx.author.mention} removed server {server} from the list of servers to listen to.')
            else:
                await ctx.send(f'{ctx.author.mention} server {server} is not being listened to.')
        else:
            await ctx.send(f'{ctx.author.mention} you do not have permission to use this command.')
    
    @commands.command(aliases=['sub'])
    async def subscribe(self, ctx, server, user):
        bot = self.bot
        if ctx.author.guild_permissions.administrator:
            if server not in bot.subscribers_:
                # validate input
                if server not in bot.listeners:
                    await ctx.send(f'{ctx.author.mention} server {server} is not being listened to.')
                    return
                elif not await bot.get_guild(int(server)).fetch_member(int(user)).guild_permissions.administrator:
                    await ctx.send(f'{ctx.author.mention} user {user} is not an admin in server {server}.')
                    return
                elif await ctx.guild.fetch_member(int(user)) == None:
                bot.subscribers_.append({'server': server, 'user': user, 'server2': server2})
                with open('/saves/bannotif/subscribers.p', 'wb') as f:
                    pickle.dump(bot.subscribers_, f)
                await ctx.send(f'{ctx.author.mention} added subscription for user {user} in server {server} to server {server2}.')
            else:
                await ctx.send(f'{ctx.author.mention} user {user} is already subscribed to server {server}.')
        else:
            await ctx.send(f'{ctx.author.mention} you do not have permission to use this command.')
