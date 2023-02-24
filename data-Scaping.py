# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 23:32:24 2023

@author: spika
"""
import requests
import random
from riotwatcher import LolWatcher, ApiError
import time
    
# watcher = LolWatcher('RGAPI-af2143e1-3872-472e-8e1b-859f6011d83c')

# my_region = 'eun1'

# summoner_name = 'spikal'

# summoner = watcher.summoner.by_name(my_region, summoner_name)

# my_ranked_stats = watcher.league.by_summoner(my_region, summoner['id']) # [0] is for solo duo





# Replace YOUR_API_KEY with your actual API key
API_KEY = "RGAPI-eda2b354-1a5b-4f18-a660-19ec570dcd1a"
# Replace REGION with the region you want to query (e.g. "na1", "euw1", etc.)
REGION = "eun1"
# Replace TIER with the tier you want to query (e.g. "GOLD")
TIER = "GOLD"

pages = ['1', '2', '3']

# Step 1: Get a list of all leagues in the region
#leagues_url = f"https://{REGION}.api.riotgames.com/lol/league/v4/leagues?api_key={API_KEY}"
random_players_url = f"https://eun1.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/{TIER}/I?page={pages[0]}&api_key={API_KEY}"



#Gets random players from all the ranks and returns a list 
def get_players():
    # TIERS = ["IRON", "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND"]
    # RANKS = ["I", "II", "III", "IV"]
    # REGIONS = ["eun1", "na1", "eu1"]
    PAGES = [1]
    TIERS = ["GOLD"]
    RANKS = ["I"]
    REGIONS = ["eun1"]
    PAGES = [1]
    result = []
    
    for PAGE in PAGES:
        for REGION in REGIONS:
            for TIER in TIERS:
                for RANK in RANKS:
                    random_players_url = f"https://{REGION}.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/{TIER}/{RANK}?page={PAGE}&api_key={API_KEY}"
                    try:
                        random_players_response = requests.get(random_players_url)
                        random_players = random_players_response.json()
                        result.append(random_players)
                    except requests.exceptions.RequestException as e:
                        print(f"Error: {e}. Retrying in 5 seconds...")
                        time.sleep(5)
                        continue
                
    return result
                
                
                

                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                