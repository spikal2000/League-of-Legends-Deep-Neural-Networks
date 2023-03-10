import requests
import random
from riotwatcher import LolWatcher, ApiError
import time
import pickle
import pandas as pd
import concurrent.futures
import numpy as np


# Replace YOUR_API_KEY with your actual API key
API_KEY = "RGAPI-c790dfab-58d6-4785-868d-85aa454a226b"
lol_watcher = LolWatcher(API_KEY)
TIERS = ["IRON", "SILVER", "GOLD", "PLATINUM", "DIAMOND"]
RANKS = ["I", "II", "III", "IV"]
REGIONS = ["eun1"]
PAGES = [1]


columns = ['match_id',
           
           'summonerLevel_b1',
           'tier_b1',
           'rank_b1',
           'leaguePoints_b1',
           'wins_b1',
           'losses_b1',
           'veteran_b1',
           'inactive_b1',
           'freshBlood_b1',
           'hotStreak_b1',
           
           'summonerLevel_b2',
           'tier_b2',
           'rank_b2',
           'leaguePoints_b2',
           'wins_b2',
           'losses_b2',
           'veteran_b2',
           'inactive_b2',
           'freshBlood_b2',
           'hotStreak_b2',
           
           'summonerLevel_b3',
           'tier_b3',
           'rank_b3',
           'leaguePoints_b3',
           'wins_b3',
           'losses_b3',
           'veteran_b3',
           'inactive_b3',
           'freshBlood_b3',
           'hotStreak_b3',
          
           'summonerLevel_b4',
           'tier_b4',
           'rank_b4',
           'leaguePoints_b4',
           'wins_b4',
           'losses_b4',
           'veteran_b4',
           'inactive_b4',
           'freshBlood_b4',
           'hotStreak_b4',
          
           'summonerLevel_b5',
           'tier_b5',
           'rank_b5',
           'leaguePoints_b5',
           'wins_b5',
           'losses_b5',
           'veteran_b5',
           'inactive_b5',
           'freshBlood_b5',
           'hotStreak_b5',
           
           
           
           'summonerLevel_r1',
           'tier_r1',
           'rank_r1',
           'leaguePoints_r1',
           'wins_r1',
           'losses_r1',
           'veteran_r1',
           'inactive_r1',
           'freshBlood_r1',
           'hotStreak_r1',
           
           
           'summonerLevel_r2',
           'tier_r2',
           'rank_r2',
           'leaguePoints_r2',
           'wins_r2',
           'losses_r2',
           'veteran_r2',
           'inactive_r2',
           'freshBlood_r2',
           'hotStreak_r2',
           
           
           'summonerLevel_r3',
           'tier_r3',
           'rank_r3',
           'leaguePoints_r3',
           'wins_r3',
           'losses_r3',
           'veteran_r3',
           'inactive_r3',
           'freshBlood_r3',
           'hotStreak_r3',
           'summonerLevel_r3',
           'tier_r3',
           'rank_r3',
           'leaguePoints_r3',
           'wins_r3',
           'losses_r3',
           'veteran_r3',
           'inactive_r3',
           'freshBlood_r3',
           'hotStreak_r3',
           'summonerLevel_r3',
           'tier_r3',
           'rank_r3',
           'leaguePoints_r3',
           'wins_r3',
           'losses_r3',
           'veteran_r3',
           'inactive_r3',
           'freshBlood_r3',
           'hotStreak_r3',
           
           'blueTeam_win']


# Define an empty DataFrame with the columns
df = pd.DataFrame(columns=columns)
# match_ids = get_match_ids()
with open('match_ids.pickle', 'rb') as f:
    match_ids = pickle.load(f)
# match_ids = match_ids[94:100]
def run():
    
    # match_ids = get_match_ids()
    for match in match_ids:
        win = 0
        blueTeam = []
        redTeam = []
        try:
            time.sleep(1.5)
            match_details = lol_watcher.match.by_id(region=REGIONS[0],  match_id=match)
            participants = match_details['metadata']['participants']
            for participant in participants:
                for i in range(0,10):
                    if participant == match_details['info']['participants'][i]['puuid']:
                        if match_details['info']['participants'][i]['teamId'] == 100:
                            blueTeam.append(match_details['info']['participants'][i]['puuid'])
                        if match_details['info']['participants'][i]['teamId'] == 200:
                            redTeam.append(match_details['info']['participants'][i]['puuid'])
            #start here
            with concurrent.futures.ThreadPoolExecutor() as executor:
                bInfo_future = executor.submit(get_participants_info, blueTeam)
                rInfo_future = executor.submit(get_participants_info, redTeam)
            
            bInfo = bInfo_future.result()
            
            # bInfo = get_participants_info(blueTeam)
            if bInfo is False:
                continue
            # rInfo = get_participants_info(redTeam)
            rInfo = rInfo_future.result()
            if rInfo is False:
                continue
           
            #teamID = 100 == blueteam
            if match_details['info']['teams'][0]['win']:
                win = 1
            
            bl = []
            rd = []
            for i in range(0,5):
                bl.append(bInfo[i]['summonerLevel'])
                bl.append(bInfo[i]['tier'])
                bl.append(bInfo[i]['rank'])
                bl.append(bInfo[i]['leaguePoints'])
                bl.append(bInfo[i]['wins'])
                bl.append(bInfo[i]['losses'])
                bl.append(bInfo[i]['veteran'])
                bl.append(bInfo[i]['inactive'])
                bl.append(bInfo[i]['freshBlood'])
                bl.append(bInfo[i]['hotStreak'])
                
                
                rd.append(rInfo[i]['summonerLevel'])
                rd.append(rInfo[i]['tier'])
                rd.append(rInfo[i]['rank'])
                rd.append(rInfo[i]['leaguePoints'])
                rd.append(rInfo[i]['wins'])
                rd.append(rInfo[i]['losses'])
                rd.append(rInfo[i]['veteran'])
                rd.append(rInfo[i]['inactive'])
                rd.append(rInfo[i]['freshBlood'])
                rd.append(rInfo[i]['hotStreak'])
               
            
            row = [match] + bl + rd + [win]   
            df.loc[len(df)] = row
            print(df)
        except ApiError as err:
            # Handle any errors that occur
            print(f"API error: {err}")
            print(f"Sleeps for 2 min...")
            time.sleep(130)
            continue
            
    return df

def get_participants_info(participants):
    print("getting participants info")
    result = {}
    for i, participant in enumerate(participants):
        time.sleep(1.5)
        summoner_obj = lol_watcher.summoner.by_puuid(REGIONS[0], participant)
        ranked_stats = lol_watcher.league.by_summoner(REGIONS[0], summoner_obj['id'])
        if len(ranked_stats) == 1:
            j = 0
        elif len(ranked_stats) == 2:
            j = 1
        else:
            print("noinfo")
            return False
            break
        result[i] = {
                    'summonerLevel':summoner_obj['summonerLevel'],
                    'tier':ranked_stats[j]['tier'],
                    'rank':ranked_stats[j]['rank'],
                    'leaguePoints':ranked_stats[j]['leaguePoints'],
                    'wins':ranked_stats[j]['wins'],
                    'losses':ranked_stats[j]['losses'],
                    'veteran':ranked_stats[j]['veteran'],
                    'inactive':ranked_stats[j]['inactive'],
                    'freshBlood':ranked_stats[j]['freshBlood'],
                    'hotStreak':ranked_stats[j]['hotStreak']
            }
    return result



def average(numbers):
    if len(numbers) == 0:
        return 0
    return sum(numbers) / len(numbers)