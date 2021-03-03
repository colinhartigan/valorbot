import os
import datetime
import valapi
from valapi import api_exception
import discord 
import asyncio
import utils, embeds
import iso8601
import match_flows


# jump-in points for the main flow
async def profile_search_flow(client,name,tag,message):
    reply = await message.channel.send("Searching for profile...")
    try:
        profile = await valapi.get_profile(name,tag)
    except api_exception as e:
        await reply.delete()
        embed = await embeds.build_error_embed(e.data[0],e.data[1],e.data[2])
        await message.channel.send(message.author.mention,embed=embed)
        return
    
    await profile_details_flow(client,name,tag,message,reply)

async def mmr_search_flow(client,name,tag,message):
    reply = await message.channel.send("Searching for user...")
    try:
        profile = await valapi.get_profile(name,tag)
    except api_exception as e:
        await reply.delete()
        embed = await embeds.build_error_embed(e.data[0],e.data[1],e.data[2])
        await message.channel.send(message.author.mention,embed=embed)
        return
    
    await competitive_info_flow(client,name,tag,message,reply)



async def profile_details_flow(client,name,tag,message,reply,back_callback=None,args=None):
    mmr = await valapi.get_mmr(name,tag)
    profile = await valapi.get_profile(name,tag)
    embed = await embeds.build_profile_details(profile,mmr)
    await reply.edit(content=message.author.mention,embed=embed)
    await reply.clear_reactions()

    reactions = ["🏅","🏆"]

    option = await utils.wait_for_reactions(client,message,reply,embed,reactions,back_callback)
    print(f'selected {option}')
    if option != -2:
        await reply.clear_reactions()
        await reply.add_reaction("⏳")
        if option == 0:
            await competitive_info_flow(client,name,tag,message,reply,back_callback=None,args=None)
        elif option == 1:
            await match_flows.match_history_flow(client,name,tag,message,reply,profile_details_flow,(client,name,tag,message,reply,back_callback,args))
        elif option == -1:
            await back_callback(*args)
    else:
        await reply.clear_reactions()
        embed.set_footer(text="")
        await reply.edit(embed=embed)


async def competitive_info_flow(client,name,tag,message,reply,back_callback=None,args=None):
    mmr = await valapi.get_mmr_history(name,tag)
    profile = await valapi.get_profile(name,tag)
    reactions = []
    embed = await embeds.build_mmr_history(mmr,profile)
    await reply.edit(content=message.author.mention,embed=embed)
    await reply.clear_reactions()