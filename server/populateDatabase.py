# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 14:02:51 2025

@author: curtis
"""
import requests
import os
from bs4 import BeautifulSoup
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

# Connect to the MongoDB database
uri = os.getenv('MONGODB_URI')
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["SpongeSearch"]
collection = db["SB_Dialogue"]

# Clear the collection
collection.delete_many({})

# Load the episode list page and HTML content
all_episodes = "https://spongebob.fandom.com/wiki/List_of_episodes_(simple)/episodes"
page = requests.get(all_episodes)

# print(page.text)

# Parse the HTML content
soup = BeautifulSoup(page.content, "html.parser")

# Retrieve the first table on the page
# In this case, the first table contains all the episode names (ONLY for the SBSP series).
episode_table = soup.find_all('table', {'class': 'wikitable'})[0]

# From this table, extract all the episode names
# Most anchor elements that have a link/href attribute contain an episode name.
links = episode_table.find_all('a', href=True)

first_links = links[:421]

# Extract transcript pages and create JSON objects for each dialogue.

for link in first_links:
    try:
        # Skip timeline links
        if link['href'].find("Timeline") != -1:
            continue

        title = link.text
        # print(title)

        # Make the title URL-compatible
        title_URL = title.replace(" ", "_")
        transcript_link = f'https://spongebob.fandom.com/wiki/{title_URL}/transcript'
        # print(transcript_link)

        transcript_page = requests.get(transcript_link)
        transcript_soup = BeautifulSoup(transcript_page.content, "html.parser")
        
        # Get title card image
        title_card = transcript_soup.find('img',{'class':'pi-image-thumbnail'})
        title_card_img = title_card['src'].split("/revision")[0]
        
        # Get general info
        general_info = transcript_soup.find(
            'section', {'class': 'pi-item pi-group pi-border-color'})

        # Get season number
        season = general_info.find(
            'div', {'class': 'pi-data-value pi-font'})
        
        season_number = 0
        if season.text.isdigit():
            season_number = int(season.text)
        
        # Get all dialogue and lines
        transcript_div = transcript_soup.find('div',{'class':'mw-content-ltr mw-parser-output'})
        dialogue = transcript_div.find_all('li')
        for line in dialogue:
            # The first bolded element should contain the character's name
            character = line.find('b')
            
            # Skip lines not said by any character
            if not character:
                continue
            
            # Separate character name and dialogue
            character_name = character.text.replace(":","").strip().lower()
            character_line = line.text.replace(character.text,"").strip()
            
            # Create a JSON document
            dialogue_object = {
                'episode_title':title,
                'season':season_number,
                'character':character_name,
                'dialogue':character_line,
                'transcript':transcript_link,
                'image':title_card_img
                }
            
            # Insert the document into the MongoDB collection
            print(dialogue_object)
            collection.insert_one(dialogue_object)
    except:
        print("An error occured.")
