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
import urllib.request;
import re;
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
		#Strips the message to be the pokemon's name, and then opens the allpokemon file
		pokemon_name = message.content[9:].lower();
		pokemon_list = open("allpokemon","r");
		strnum = "";
		pokemon_num = -1;
		#Searches the allpokemon file for the number corresponding to the specified pokemon
		for l in pokemon_list:
			#Split the lines into a string list on the comma
			name_num = l.split(",");
			#if the name is in the list, we grab it's number, otherwise we tell the user we couldn't find it
			if pokemon_name == (name_num[0]):
				pokemon_num = int(name_num[1][:3]);
				strnum = name_num[1][:3];
				await client.send_message(message.channel, pokemon_name + ": " + str(pokemon_num));
				break;
		if pokemon_num == -1:
			await client.send_message(message.channel, "Sorry, " + pokemon_name + " was not found in the pokedex, maybe you spelled it incorrectly?");
		
		#This is the link based on how serebii.net is set up
		link = "https://www.serebii.net/pokedex-sm/" + strnum + ".shtml";
		#Since urllib doesn't produce an object, but a module instead, we have to do this work-around
		#in order to get our object that we can iterate through.
		request = urllib.request.Request(link);
		opener = urllib.request.build_opener();
		response = opener.open(request);
		
		#Next we iterate through the lines of html and find the first instance of "Base Stats - Total: "
		#This is because the 6 lines after contain each stat in order of hp, atk, def, spatk, spdef, and speed.
		#For sake of simplicity, we toss it all into a list to easier shaving later.
		for line in response:
			if "Base Stats - Total: " in line:
				#Grabs all of the lines that we need, we'll shave off the bs afterwards
				rawStats = [response[response.index(line)+1],response[response.index(line)+2],response[response.index(line)+3],response[response.index(line)+4],response[response.index(line)+5],response[response.index(line)+6]];
				break;
		#Now we shave off the bs
		for stats in rawStats:
			stats = re.split("(<+|>+)",stats);


		"""
		THINGS TO LOOK FOR IN A PAGE:
		<option value="/pokedex-sm/NUMBER HERE.shtml">POKEMON NAME HERE</option>
		--> or we can just format the user's input since it has to be correct anyways 
		--> SAME THING WITH THE NUMBER

		STATS:
		--> so the stats are formatted retardedly cuz what is good css and html
			<td align="center" class="fooevo">HP</td>
			<td align="center" class="fooevo">Attack</td>
			<td align="center" class="fooevo">Defense</td>
			<td align="center" class="fooevo">Sp. Attack</td>
			<td align="center" class="fooevo">Sp. Defense</td>
			<td align="center" class="fooevo">Speed</td></tr>
		CORRESPONDS TO:
			<td align="center" class="fooinfo">105</td>
			<td align="center" class="fooinfo">150</td>
			<td align="center" class="fooinfo">90</td>
			<td align="center" class="fooinfo">150</td>
			<td align="center" class="fooinfo">90</td>
			<td align="center" class="fooinfo">95</td></tr>
		----> FIND THE FIRST INSTANCE OF "Base Stats - Total: "
			--> STORE THE THE FIRST SIX LINES AFTER THAT
			--> SPLIT THEM ON < AND >
			--> GRAB THE THIRD ELEMENT OF EACH RESULTING LIST (will be the base stats at lvl 100)
		FINDING THE TYPE OF THE POKEMON IS ACTUALLY AIDS CUZ WHAT IS GOOD CSS AND HTML????
		--> excellent work around: post the link as well
		"""

	#Type @Poke-Bot to get a quick blurb of info about the bot
	if message.content.startswith("<@369661689723092992>"):
		await client.send_message(message.channel, "Created by Bartosz Kosakowski. Type !pokebot <pokemon name> to retrieve data about a pokemon!");

client.run('MzY5NjYxNjg5NzIzMDkyOTky.DMbx6A.7V7YXFh5MEdEON2q29CCk8FoKEw');