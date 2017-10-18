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
from bs4 import BeautifulSoup;

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
	botmessage = "";
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
				botmessage += "Name: " + name_num[0].title() + "\n" + "National number: " + name_num[1] + "\n";
				strnum = name_num[1][:3];
				break;
		if pokemon_num == -1:
			await client.send_message(message.channel, "Sorry, " + pokemon_name + " was not found in the pokedex, maybe you spelled it incorrectly?");
		
		#This is the link based on how serebii.net is set up
		link = "https://www.serebii.net/pokedex-sm/" + strnum + ".shtml";
		"""
		We try to connect to the site (probably poorly worded but I dunno enough about
		networks and whatnot to validate it), and catch+print the error if the url is
		incorrect.
		"""
		try:
			response = urllib.request.urlopen(link);
		except urllib.error.URLError as e:
			print(e.reason);
		else:
			#If successful, we read the html in the page
			html = response.read();
			
			#================
			#This block is to check the encoding of the page so we can convert it to a string
			soup = BeautifulSoup(html, "html.parser");
			decoded_page = html.decode(str(soup.original_encoding));
			#================
			
			pagesplit = decoded_page.split("\n");
			#Filters out the empty strings that get generated (ie, "")
			pagesplit = list(filter(None, pagesplit));

			#THIS SECTION GRABS ALL OF THE STATS FOR THE POKEMON
			#Finds the first instance of "Base Stats - Total:" since the lines after contain the stats
			for l in pagesplit:
				if "Base Stats - Total:" in l:
					statline = pagesplit.index(l);
					#We use this to create a list containing the stats, but are surrounded by html junk
					rawstats = [pagesplit[statline+1],pagesplit[statline+2],pagesplit[statline+3],pagesplit[statline+4],pagesplit[statline+5],pagesplit[statline+6]];
					break;
			#Shaves off the bs and leaves only the stats as a list of strings
			stats = [];
			for s in rawstats:
				s = re.split("(<+|>+)",s);
				stats.append(s[4]);
			
			botmessage += "---STATS---\n" + "HP: " + stats[0] + "\n" + "Attack: " + stats[1] + "\n" + "Defense: " + stats[2] + "\n" + "Sp. attack: " + stats[3] + "\n" + "Sp. defense: " + stats[4] + "\n" + "Speed: " + stats[5] + "\n";
			botmessage += "\nFor more info visit: " + link;

			#Sends the message with info in it
			await client.send_message(message.channel, botmessage);

	#Type @Poke-Bot to get a quick blurb of info about the bot
	if message.content.startswith("<@369661689723092992>"):
		await client.send_message(message.channel, "Created by Bartosz Kosakowski. Type !pokebot <pokemon name> to retrieve data about a pokemon!");

client.run('MzY5NjYxNjg5NzIzMDkyOTky.DMbx6A.7V7YXFh5MEdEON2q29CCk8FoKEw');