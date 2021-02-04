from dotenv import load_dotenv
import os
import datetime
import valapi
from valapi import api_exception
import discord 
import asyncio
import assets, embeds
import iso8601
import match_flows, profile_flows

load_dotenv()

TOKEN = os.getenv('TOKEN')

client = discord.Client()

@client.event
async def on_ready():  
    print("Ready!")

@client.event
async def on_message(message):
    split = message.content.split(" ")
    command = split[0]
    #print(split)
    if command.startswith("/latest"):
        await message.channel.trigger_typing()
        user = split[1].split("#")
        name = user[0]
        tag = user[1]
        await match_flows.latest_match_flow(client,name,tag,message)


    if command.startswith("/profile"):
        await message.channel.trigger_typing()
        user = split[1].split("#")
        name = user[0]
        tag = user[1]
        await profile_flows.profile_search_flow(client,name,tag,message)
        

    if command.startswith("/history"):
        await message.channel.trigger_typing()
        user = split[1].split("#")
        name = user[0]
        tag = user[1]
        await match_flows.match_history_flow(client,name,tag,message)






client.run(TOKEN)