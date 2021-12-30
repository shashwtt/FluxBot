import discord

from discord.ext import commands
import hex_colors

colors = hex_colors.colors


class Ban(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='ban', help='Ban a member from the server', usage='<member> <reason>')
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member:discord.Member, *, reason="No reason provided"): #Default reason is "No reason provided"
        if member == self.client.user: #If  the 'member' is the bot
            await ctx.send("I don't know what the procedure is here, but I cannot leave like this. You'll have to remove me from the server manually. If I caused any problem, DM it to me, with details so my developer can fix me.")
            return

        #If the 'member' is the person who invoked the command
        if member == ctx.author:
            await ctx.send("Why do you wanna ban your self?")
            return

        # Checking if the other person has a higher or same role
        if member.top_role.position > ctx.author.top_role.position:
            await ctx.send(f"{member.mention} has a higher role than you. You cannot ban them")
            return

        if member.top_role.position == ctx.author.top_role.position:
            await ctx.send(f"{member.mention} has the same top role as you. You cannot ban them.")
            return

        # Checking if the other person has a higher role than the bot
        if member.top_role.position > ctx.guild.me.top_role.position:
            await ctx.send(f"{member} has a higher role than me. I can't ban them.")
            return

        if member.top_role.position == ctx.guild.me.top_role.position:
            await ctx.send(f"{member} has the same top role as me. I cannot ban them.")
            return

        #Embed to be sent to the member
        m_em = discord.Embed(color=hex_colors.m_red)
        m_em.set_author(name=f"{ctx.author} banned you from {ctx.guild.name}", icon_url=ctx.author.avatar.url)
        m_em.set_thumbnail(url=ctx.guild.icon_url)
        m_em.add_field(name="Reason", value=reason)

        #Embed to be sent in the channel
        em = discord.Embed(color=hex_colors.m_red)
        em.set_author(name=f"{ctx.author} banned {member}", icon_url=ctx.author.avatar.url)
        em.set_thumbnail(url=member.avatar.url)
        em.add_field(name='Reason:', value=reason)

        try:
            await member.send(embed=m_em)
        except:
            pass

        await member.ban(reason=reason)
        await ctx.send(embed=em)

def setup(client):
    client.add_cog(Ban(client))