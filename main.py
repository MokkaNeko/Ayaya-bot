import discord
from discord.ext import commands
import os
import random
import asyncio
from dotenv import load_dotenv
import music_cog

load_dotenv()

c_credit = """
```Ayaya bot
Created by Iksanard
Discord : Iksanard#6022
Hope you enjoy``` """

bot = commands.Bot(command_prefix=">>")
filtered_words = ["kontol"]

#Bot Ready
@bot.event
async def on_ready():
    print("we have logged in as {0.user}".format(bot))

#status
async def change_pres():
    await bot.wait_until_ready()
    statuses = ["with Furry Vornogiri | >>help", "Garut.3gp | >>help"]
    while not bot.is_closed():
        status = random.choice(statuses)
        await bot.change_presence(activity=discord.Game(name=status))
        await asyncio.sleep(5)

#Help
@bot.command(alias=["hello", "hi", "halo", "konnichiwa"])
async def greeting(ctx):
    await ctx.reply("Hello!")

@bot.command()
async def credit(ctx):
    await ctx.reply(c_credit)

#Moderation
@bot.command(aliases=["c"])
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit = amount)

@bot.event
async def on_message(msg):
    for word in filtered_words:
        if word in msg.content:
            await msg.delete()
    await bot.process_commands(msg)

@bot.command(aliases=["slave", "r"])
@commands.has_permissions(kick_members=True)
async def restrict(ctx, member:discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Slave")
    await member.add_roles(role)
    await ctx.send(f"{member.display_name} got slaved lmao")

@bot.command(aliases=["ur", "us"])
@commands.has_permissions(administrator=True)
async def unrestrict(ctx, member:discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Slave")
    await member.remove_roles(role)
    await ctx.send(f"{member.display_name} you got unslaved yaay")

@bot.command(aliases=["k"])
@commands.has_permissions(kick_members=True)
async def kick(ctx, member:discord.Member, *, reason="no reason"):
    await member.kick(reason=reason)
    await ctx.send("{member} have been kicked from {server}, because ".format(member = member, server = ctx.message.guild.name) + reason)

@bot.command(aliases=["b"])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member:discord.Member, *, reason="no reason"):
    await member.ban(reason=reason)
    await ctx.send("{member} have been kicked from {server}, because ".format(member = member, server = ctx.message.guild.name) + reason)

@bot.command(aliases=["ub"])
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_disc = member.split("#")
    for banned_entry in banned_users:
        user = banned_entry.user
        if(user.name, user.discriminator) == (member_name, member_disc):
            await ctx.guild.unban(user)
            await ctx.send(member_name + " has benn unbanned!")
            return
    await ctx.send(member + " not found or was not banned!")

#info
@bot.command(aliases=["user"])
async def info(ctx, member:discord.Member):
    embed = discord.Embed(title = member.display_name, description = member.mention, color = discord.Colour.teal())
    embed.add_field(name = "ID", value = member.id, inline = True)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"requested by{ctx.author.display_name}")
    await ctx.send(embed = embed)

@bot.command(aliases=["ava"])
async def avatar(ctx, member:discord.Member):
    embed = discord.Embed(title = f"this is {member.display_name}'s avatar", color = discord.Colour.teal())
    embed.set_image(url=member.avatar_url)
    await ctx.send(embed=embed)

@bot.command()
async def server(ctx):
    embed = discord.Embed(title = "Server Info", color = discord.Colour.teal())
    embed.add_field(name= "Server Name", value=ctx.guild.name, inline=False)
    embed.add_field(name= "Server ID", value=ctx.guild.id, inline=False)
    embed.add_field(name= "Date Created", value=ctx.guild.created_at, inline=True)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    await ctx.send(embed=embed)

#music
bot.add_cog(music_cog.music_cog(bot))

#error
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("you can't do that")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("did you miss something??")
    else:
        raise error

#run
bot.loop.create_task(change_pres())
bot.run("OTEwNDM2NTU3MDcxMjE2Njgw.GmYqAw.OQCYmt-aAu0iGJV6EGRPvj-p8KcoF9RdxcD8Vw")
