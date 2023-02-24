# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 23:32:24 2023

@author: spika
"""
import requests
import random
from riotwatcher import LolWatcher, ApiError
import time
import pickle
    
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

PAGES = [1]

# Step 1: Get a list of all leagues in the region
#leagues_url = f"https://{REGION}.api.riotgames.com/lol/league/v4/leagues?api_key={API_KEY}"
# random_players_url = f"https://eun1.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/{TIER}/I?page={pages[0]}&api_key={API_KEY}"



#Gets random players from all the ranks and returns a list 
#NOte: we dont have to use this, get_puuids() is ussing this for us
def get_players():
    # TIERS = ["IRON", "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND"]
    # RANKS = ["I", "II", "III", "IV"]
    # REGIONS = ["eun1", "na1", "eu1"]
    # PAGES = [1]
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


def get_puuids():
    players = get_players()
    
    puuids = []
    for page in range(0, len(PAGES)):
        for player in players[page]:
            player_puuid_url = f"https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{player['summonerName']}?api_key={API_KEY}"
            try:
                player_puuid_response = requests.get(player_puuid_url)
                if player_puuid_response.status_code == 404:
                    print("Player not found.")
                    continue
                elif player_puuid_response.status_code == 429:
                    print("Rate limit exceeded. Waiting for 2 min...")
                    time.sleep(130)
                    player_puuid_response = requests.get(player_puuid_url)
                    player_puuid = player_puuid_response.json()
                    puuid = player_puuid['puuid']
                    puuids.append(puuid)
                else:
                    player_puuid = player_puuid_response.json()
                    puuid = player_puuid['puuid']
                    puuids.append(puuid)
                    time.sleep(5)
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}. Retrying in 5 seconds...")
                time.sleep(5)
                continue
            
    return puuids
            
            



    


def get_match_ids():
    # puuids = get_puuids()
    # with open('puuids.pickle', 'wb') as f:
    #     pickle.dump(puuids, f)
    # with open('puuids.pickle', 'rb') as f:
    #     puuids = pickle.load(f)
    
    puuids = ["xKkamFA9ysY6dCEvcTCSkAeCl2I0LFqLDhMxvSPJS3q-JRXa64rc5UlFJ9mV338APusxaJodwh3UoQ", "Iuk2x32ujlq_Bpr_JTEHm7gIDd_TlwYNh4XLZyWdP3PTn-L4heP8u0EUmqVQyB54Efcaym8zAnSIew"]
    
    number_of_matches = 1
    player_matchId = {}
    for puuid in puuids:
        # GET A PLAYERS IDS MATCH HISTRY USING PUUI...
        #https://developer.riotgames.com/apis#match-v5/GET_getMatchIdsByPUUID
        match_ids = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={number_of_matches}&api_key={API_KEY}"
        try:
            match_response = requests.get(match_ids)
            if match_response.status_code == 404:
                print("match not found.")
                continue
            elif match_response.status_code == 429:
                print("Rate limit exceeded. Waiting for 2 min...")
                time.sleep(130)
                match_response = requests.get(match_ids)
                matches_ids = match_response.json()
                player_matchId[puuid] = matches_ids
            else:
                matches_ids = match_response.json()
                player_matchId[puuid] = matches_ids
                time.sleep(5)
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}. Retrying in 5 seconds...")
            time.sleep(5)
            continue
    
    
    return player_matchId






                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                