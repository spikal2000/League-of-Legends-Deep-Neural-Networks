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
import pandas as pd
import concurrent.futures
    
# watcher = LolWatcher('RGAPI-af2143e1-3872-472e-8e1b-859f6011d83c')

# my_region = 'eun1'

# summoner_name = 'spikal'

# summoner = watcher.summoner.by_name(my_region, summoner_name)

# my_ranked_stats = watcher.league.by_summoner(my_region, summoner['id']) # [0] is for solo duo



# Replace YOUR_API_KEY with your actual API key
API_KEY = "RGAPI-f7bd360b-0bcc-48ea-8244-a2e81c52ae71"
lol_watcher = LolWatcher(API_KEY)
TIERS = ["GOLD"]
RANKS = ["I"]
REGIONS = ["eun1"]
PAGES = [1]


#Gets random players from all the ranks and returns a list 
#NOte: we dont have to use this, get_puuids() is ussing this for us
def get_players():
    print('geting the players')
    #TIERS = ["GOLD"]
    #RANKS = ["I"]
    #REGIONS = ["eun1"]
    #PAGES = [1]
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
    # with open('players.pickle', 'wb') as f:
    #     pickle.dump(result, f)
    return result


def get_puuids():
    print("geting the puuids")
    players = get_players()
    players  = [val for sublist in players for val in sublist]
    # with open('players.pickle', 'rb') as f:
        # players = pickle.load(f)
    puuids = []
    for player in players:
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
    puuids = get_puuids()
    # with open('puuids.pickle', 'wb') as f:
    #     pickle.dump(puuids, f)
    # with open('puuids.pickle', 'rb') as f:
    #     puuids = pickle.load(f)
    
    #puuids = ["xKkamFA9ysY6dCEvcTCSkAeCl2I0LFqLDhMxvSPJS3q-JRXa64rc5UlFJ9mV338APusxaJodwh3UoQ", "Iuk2x32ujlq_Bpr_JTEHm7gIDd_TlwYNh4XLZyWdP3PTn-L4heP8u0EUmqVQyB54Efcaym8zAnSIew"]
    
    number_of_matches = 1
    matches = []
    for puuid in puuids:
        # GET A PLAYERS IDS MATCH HISTRY USING PUUI...
        #https://developer.riotgames.com/apis#match-v5/GET_getMatchIdsByPUUID
        # match_ids = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={number_of_matches}&api_key={API_KEY}"
         #420 means its the ranked solo duo
        try:
            match_ids = lol_watcher.match.matchlist_by_puuid(region=REGIONS[0], puuid=puuid, queue=420)
            matches.append(match_ids)
            time.sleep(2)
        except ApiError as err:
            # Handle any errors that occur
            print(f"API error: {err}")
            time.sleep(130)
            continue
    matches  = [val for sublist in matches for val in sublist]
    
    return matches
'kills': average(kills), 
             'deaths': average(deaths), 
             'assists': average(assists),
             'visionScore': average(visionScore),
             'wardsKilled': average(wardsKilled),
             'goldPerMinute': average(goldPerMinute),
             'landSkillShotsEarlyGame': average(landSkillShotsEarlyGame),
             'skillshotsHit':average(skillshotsHit),
             'skillshotsDodged':average(skillshotsDodged),
             'turretTakedowns':average(turretTakedowns),
             'goldEarned':average(goldEarned),
             'onMyWayPings':average(onMyWayPings),
             'damagePerMinute':average(damagePerMinute),
             'dodgeSkillShotsSmallWindow':average(dodgeSkillShotsSmallWindow),
             'laneMinionsFirst10Minutes':average(laneMinionsFirst10Minutes),
             'soloKills':average(soloKills),
             'dancedWithRiftHerald':average(dancedWithRiftHerald)}

# Define the columns for the DataFrame
columns = ['match_id',
           'average_kills-red_Player1', 'average_kills-red_Player2', 'average_kills-red_Player3', 'average_kills-red_Player4', 'average_kills-red_Player5',
           'average_kills-Blue_player1', 'average_kills-Blue_player2', 'average_kills-Blue_player3', 'average_kills-Blue_player4', 'average_kills-Blue_player5',
           'average_deaths-red_Player1', 'average_deaths-red_Player2', 'average_deaths-red_Player3', 'average_deaths-red_Player4', 'average_deaths-red_Player5',
           'average_deaths-Blue_player1', 'average_deaths-Blue_player2', 'average_deaths-Blue_player3', 'average_deaths-Blue_player4', 'average_deaths-Blue_player5',
           
           'average_assists-red_Player1', 'average_assists-red_Player2', 'average_assists-red_Player3', 'average_assists-red_Player4', 'average_assists-red_Player5',
           'average_assists-Blue_player1', 'average_assists-Blue_player2', 'average_assists-Blue_player3', 'average_assists-Blue_player4', 'average_assists-Blue_player5',
           
           'average_visionScore-red_Player1', 'average_visionScore-red_Player2', 'average_visionScore-red_Player3', 'average_visionScore-red_Player4', 'average_visionScore-red_Player5',
           'average_visionScore-Blue_player1', 'average_visionScore-Blue_player2', 'average_visionScore-Blue_player3', 'average_visionScore-Blue_player4', 'average_visionScore-Blue_player5',
           
           'average_wardsKilled-red_Player1', 'average_wardsKilled-red_Player2', 'average_wardsKilled-red_Player3', 'average_wardsKilled-red_Player4', 'average_wardsKilled-red_Player5',
           'average_wardsKilled-Blue_player1', 'average_wardsKilled-Blue_player2', 'average_wardsKilled-Blue_player3', 'average_wardsKilled-Blue_player4', 'average_wardsKilled-Blue_player5',
           
           'average_goldPerMinute-red_Player1', 'average_goldPerMinute-red_Player2', 'average_goldPerMinute-red_Player3', 'average_goldPerMinute-red_Player4', 'average_goldPerMinute-red_Player5',
           'average_goldPerMinute-Blue_player1', 'average_goldPerMinute-Blue_player2', 'average_goldPerMinute-Blue_player3', 'average_goldPerMinute-Blue_player4', 'average_goldPerMinute-Blue_player5',
           
           'average_landSkillShotsEarlyGame-red_Player1', 'average_landSkillShotsEarlyGame-red_Player2', 'average_landSkillShotsEarlyGame-red_Player3', 'average_landSkillShotsEarlyGame-red_Player4', 'average_landSkillShotsEarlyGame-red_Player5',
           'average_landSkillShotsEarlyGame-Blue_player1', 'average_landSkillShotsEarlyGame-Blue_player2', 'average_landSkillShotsEarlyGame-Blue_player3', 'average_landSkillShotsEarlyGame-Blue_player4', 'average_landSkillShotsEarlyGame-Blue_player5',
           
           'average_skillshotsHit-red_Player1', 'average_skillshotsHit-red_Player2', 'average_skillshotsHit-red_Player3', 'average_skillshotsHit-red_Player4', 'average_skillshotsHit-red_Player5',
           'average_skillshotsHit-Blue_player1', 'average_skillshotsHit-Blue_player2', 'average_skillshotsHit-Blue_player3', 'average_skillshotsHit-Blue_player4', 'average_skillshotsHit-Blue_player5',
           
           'average_skillshotsDodged-red_Player1', 'average_skillshotsDodged-red_Player2', 'average_skillshotsDodged-red_Player3', 'average_skillshotsDodged-red_Player4', 'average_skillshotsDodged-red_Player5',
           'average_skillshotsDodged-Blue_player1', 'average_skillshotsDodged-Blue_player2', 'average_skillshotsDodged-Blue_player3', 'average_skillshotsDodged-Blue_player4', 'average_skillshotsDodged-Blue_player5',
           
           'average_turretTakedowns-red_Player1', 'average_turretTakedowns-red_Player2', 'average_turretTakedowns-red_Player3', 'average_turretTakedowns-red_Player4', 'average_turretTakedowns-red_Player5',
           'average_turretTakedowns-Blue_player1', 'average_turretTakedowns-Blue_player2', 'average_turretTakedowns-Blue_player3', 'average_turretTakedowns-Blue_player4', 'average_turretTakedowns-Blue_player5',
           
           'average_goldEarned-red_Player1', 'average_goldEarned-red_Player2', 'average_goldEarned-red_Player3', 'average_goldEarned-red_Player4', 'average_goldEarned-red_Player5',
           'average_goldEarned-Blue_player1', 'average_goldEarned-Blue_player2', 'average_goldEarned-Blue_player3', 'average_goldEarned-Blue_player4', 'average_goldEarned-Blue_player5',
           
           'average_onMyWayPings-red_Player1', 'average_onMyWayPings-red_Player2', 'average_onMyWayPings-red_Player3', 'average_onMyWayPings-red_Player4', 'average_onMyWayPings-red_Player5',
           'average_onMyWayPings-Blue_player1', 'average_onMyWayPings-Blue_player2', 'average_onMyWayPings-Blue_player3', 'average_onMyWayPings-Blue_player4', 'average_onMyWayPings-Blue_player5',
           
           'average_damagePerMinute-red_Player1', 'average_damagePerMinute-red_Player2', 'average_damagePerMinute-red_Player3', 'average_damagePerMinute-red_Player4', 'average_damagePerMinute-red_Player5',
           'average_damagePerMinute-Blue_player1', 'average_damagePerMinute-Blue_player2', 'average_damagePerMinute-Blue_player3', 'average_damagePerMinute-Blue_player4', 'average_damagePerMinute-Blue_player5',
           
           'average_dodgeSkillShotsSmallWindow-red_Player1', 'average_dodgeSkillShotsSmallWindow-red_Player2', 'average_dodgeSkillShotsSmallWindow-red_Player3', 'average_dodgeSkillShotsSmallWindow-red_Player4', 'average_dodgeSkillShotsSmallWindow-red_Player5',
           'average_dodgeSkillShotsSmallWindow-Blue_player1', 'average_dodgeSkillShotsSmallWindow-Blue_player2', 'average_dodgeSkillShotsSmallWindow-Blue_player3', 'average_dodgeSkillShotsSmallWindow-Blue_player4', 'average_dodgeSkillShotsSmallWindow-Blue_player5',
           
           'average_laneMinionsFirst10Minutes-red_Player1', 'average_laneMinionsFirst10Minutes-red_Player2', 'average_laneMinionsFirst10Minutes-red_Player3', 'average_laneMinionsFirst10Minutes-red_Player4', 'average_laneMinionsFirst10Minutes-red_Player5',
           'average_laneMinionsFirst10Minutes-Blue_player1', 'average_laneMinionsFirst10Minutes-Blue_player2', 'average_laneMinionsFirst10Minutes-Blue_player3', 'average_laneMinionsFirst10Minutes-Blue_player4', 'average_laneMinionsFirst10Minutes-Blue_player5',
           
           'average_soloKills-red_Player1', 'average_soloKills-red_Player2', 'average_soloKills-red_Player3', 'average_soloKills-red_Player4', 'average_soloKills-red_Player5',
           'average_soloKills-Blue_player1', 'average_soloKills-Blue_player2', 'average_soloKills-Blue_player3', 'average_soloKills-Blue_player4', 'average_soloKills-Blue_player5',
           
           'average_danceWithRiftHerald-red_Player1', 'average_danceWithRiftHerald-red_Player2', 'average_danceWithRiftHerald-red_Player3', 'average_danceWithRiftHerald-red_Player4', 'average_danceWithRiftHerald-red_Player5',
           'average_danceWithRiftHerald-Blue_player1', 'average_danceWithRiftHerald-Blue_player2', 'average_danceWithRiftHerald-Blue_player3', 'average_danceWithRiftHerald-Blue_player4', 'average_danceWithRiftHerald-Blue_player5',
           'blueTeam_win']

# Define an empty DataFrame with the columns
df = pd.DataFrame(columns=columns)

def run():
    
    match_ids = get_match_ids()
    for match in match_ids:
        win = 0
        blueTeam = []
        redTeam = []
        try:
            match_details = lol_watcher.match.by_id(region=REGIONS[0],  match_id=match)
            participants = match_details['metadata']['participants']
            for participant in participants:
                for i in range(0,10):
                    if participant == match_details['info']['participants'][i]['puuid']:
                        if match_details['info']['participants'][i]['teamId'] == 100:
                            blueTeam.append(participant)
                        if match_details['info']['participants'][i]['teamId'] == 200:
                            redTeam.append(participant)
            #start here
            with concurrent.futures.ThreadPoolExecutor() as executor:
                bInfo_future = executor.submit(get_participants_info, blueTeam)
                rInfo_future = executor.submit(get_participants_info, redTeam)
            
            bInfo = bInfo_future.result()
            rInfo = rInfo_future.result()
            # bInfo = get_participants_info(blueTeam)
            # rInfo = get_participants_info(redTeam)
            #teamID = 100 == blueteam
            if match_details['info']['teams'][0]['win']:
                win = 1
            
            bl = []
            rd = []
            for i in range(0,5):
                bl.append(bInfo[i]['kills'])
                bl.append(bInfo[i]['deaths'])
                rd.append(rInfo[i]['kills'])
                rd.append(rInfo[i]['deaths'])
            row = [match] + rd + bl + [win]
            df.loc[len(df)] = row
            print(row)
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
    i = 0
    for participant in participants:
        time.sleep(2)
        try:
            match_history = lol_watcher.match.matchlist_by_puuid(region=REGIONS[0], puuid=participant, queue=420)
            kills = []
            deaths = []
            assists = []
            visionScore = []
            wardsKilled = []
            goldPerMinute = []
            landSkillShotsEarlyGame = []
            skillshotsHit = []
            skillshotsDodged = []
            turretTakedowns = []
            goldEarned = []
            onMyWayPings = []
            damagePerMinute = []
            dodgeSkillShotsSmallWindow = []
            laneMinionsFirst10Minutes = []
            soloKills = []
            dancedWithRiftHerald = []
            for match_id in match_history[:10]:
                time.sleep(2)
                try:
                    match_details = lol_watcher.match.by_id(region=REGIONS[0],  match_id=match_id)
                    for participant_identity in match_details['info']['participants']:
                        if participant_identity['puuid'] == participant:
                            kills.append(participant_identity['kills'])
                            deaths.append(participant_identity['deaths'])
                            assists.append(participant_identity['assists'])
                            visionScore.append(participant_identity['visionScore'])
                            wardsKilled.append(participant_identity['wardsKilled'])
                            goldPerMinute.append(participant_identity['goldPerMinute'])
                            landSkillShotsEarlyGame.append(participant_identity['landSkillShotsEarlyGame'])
                            skillshotsHit.append(participant_identity['skillshotsHit'])
                            skillshotsDodged.append(participant_identity['skillshotsDodged'])
                            turretTakedowns.append(participant_identity['turretTakedowns'])
                            goldEarned.append(participant_identity['goldEarned'])
                            onMyWayPings.append(participant_identity['onMyWayPings'])
                            damagePerMinute.append(participant_identity['damagePerMinute'])
                            dodgeSkillShotsSmallWindow.append(participant_identity['dodgeSkillShotsSmallWindow'])
                            laneMinionsFirst10Minutes.append(participant_identity['laneMinionsFirst10Minutes'])
                            soloKills.append(participant_identity['soloKills'])
                            dancedWithRiftHerald.append(participant_identity['dancedWithRiftHerald'])
                except ApiError as err:
                    print(f"API error: {err}")
                    continue
            result[i] = {'kills': average(kills), 
                         'deaths': average(deaths), 
                         'assists': average(assists),
                         'visionScore': average(visionScore),
                         'wardsKilled': average(wardsKilled),
                         'goldPerMinute': average(goldPerMinute),
                         'landSkillShotsEarlyGame': average(landSkillShotsEarlyGame),
                         'skillshotsHit':average(skillshotsHit),
                         'skillshotsDodged':average(skillshotsDodged),
                         'turretTakedowns':average(turretTakedowns),
                         'goldEarned':average(goldEarned),
                         'onMyWayPings':average(onMyWayPings),
                         'damagePerMinute':average(damagePerMinute),
                         'dodgeSkillShotsSmallWindow':average(dodgeSkillShotsSmallWindow),
                         'laneMinionsFirst10Minutes':average(laneMinionsFirst10Minutes),
                         'soloKills':average(soloKills),
                         'dancedWithRiftHerald':average(dancedWithRiftHerald)}
            i+=1
        except ApiError as err:
            # Handle any errors that occur
            print(f"API error: {err}")
            time.sleep(130)
            continue
    return result



def average(numbers):
    if len(numbers) == 0:
        return 0
    return sum(numbers) / len(numbers)

  