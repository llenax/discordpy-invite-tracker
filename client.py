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

invites_dict = {} # Store

token = "Bot_token"
prefix = "!"

client = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())

@client.event
async def on_ready():
    for guild in client.guilds:
        await set_invites(guild)
    
@client.event
async def on_invite_create(invite):
    await set_invites(invite.guild)


@client.event
async def on_invite_delete(invite):
    await set_invites(invite.guild)


@client.event
async def on_member_join(member):
    if not member.bot:
        global invites_dict
        guild = member.guild
        guild_invites = await guild.invites()
        for invite in guild_invites:
            try:
                for invite_dict in invites_dict.get(guild.id):
                    if invite_dict[0] == invite.code:
                        if int(invite.uses) > invite_dict[1]:
                            print(f"{member} joined. Invited with: {invite.code} | by {invite.inviter}")
            except Exception as error:
                print(error)
    else:
        print("Someone joined server. It could be a bot.")


async def set_invites(guild):
    guild_invites = await guild.invites()
    invites_dict[guild.id] = [tuple((invite.code, invite.uses)) for invite in guild_invites]


client.run(token)