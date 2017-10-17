"""
Poke-Bot
Created by Bartosz Kosakowski
This bot can be used like a pokedex! Type !pokebot <pokemon name>
and it will pull the image, name, nat num, type(s), abilities, and
base stats.
"""

#important link for personal reference https://discordapp.com/oauth2/authorize?&client_id=[CLIENT_ID]&scope=bot&permissions=0
#[CLIENT_ID] is supposed to be whatever code is on the dev page.
import discord;
import asyncio;
import urllib;
from random import *;

#=-=-=Global vars and whatnot=-=-=
client = discord.Client();

#Logs the bot into the server
@client.event
async def on_ready():
    print('Logged in as');
    print(client.user.name);
    print(client.user.id);
    print('------');

#Checks the message for a specific string (ie, that the bot is being called)
@client.event
async def on_message(message):
	#to do
	if message.content.startswith("!pokebot"):
		pokemon_name = message.content[9:].lower();
		await client.send_message(message.channel, pokemon_name);

	#Type @Poke-Bot to get a quick blurb of info about the bot
	if message.content.startswith("<@369661689723092992>"):
		await client.send_message(message.channel, "Created by Bartosz Kosakowski. Type !pokebot <pokemon name> to retrieve data about a pokemon!");

client.run('MzY5NjYxNjg5NzIzMDkyOTky.DMbx6A.7V7YXFh5MEdEON2q29CCk8FoKEw');