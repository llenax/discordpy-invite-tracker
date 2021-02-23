"""
Copyright (c) 2021 llenax

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import discord
from discord.ext import commands

invites_dict = {}

log = 813158187921965106  # YOUR CHANNEL ID

token = "YOUR TOKEN"

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())


async def set_invites(guild):
    guild_invites = await guild.invites()
    temp = [tuple((invite.code, invite.uses)) for invite in guild_invites]
    invites_dict[guild.id] = temp


@client.event
async def on_ready():
    for guild in client.guilds:
        await set_invites(guild)
    print("online")


@client.event
async def on_invite_create(invite):
    await set_invites(invite.guild)


@client.event
async def on_invite_delete(invite):
    await set_invites(invite.guild)


@client.event
async def on_member_join(member):
    guild = member.guild
    log_channel = discord.utils.get(member.guild.channels, id=log)
    embed = discord.Embed(color=discord.Color.blurple())
    if not member.bot:
        global invites_dict
        guild_invites = await guild.invites()

        for invite in guild_invites:
            try:
                for invite_dict in invites_dict.get(guild.id):
                    if invite_dict[0] == invite.code:
                        if int(invite.uses) > invite_dict[1]:
                            if log_channel is not None:
                                embed.description = f"{member.mention} joined server. Invited by {invite.inviter.mention}"
                                embed.add_field(
                                    name="Used Invite",
                                    value=
                                    f"Inviter: (`{invite.inviter.name}#{invite.inviter.discriminator}`) | `{invite.inviter.id}`\nHave **{invite.uses}** uses."
                                )
                                await log_channel.send(embed=embed)
            except:  #exception as e:
                pass  #print(e)
    else:
        embed.description = f"{member.mention} joined server and its a bot."
        await log_channel.send(embed=embed)


@client.event
async def on_member_remove(member):
    guild = member.guild
    await set_invites(guild)


client.run(token)