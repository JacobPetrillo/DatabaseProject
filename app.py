'''
Jacob Petrillo
Fall 2020
COP4710
'''

from flask import Flask, render_template, request, session
import sqlite3 as sql
import requests
import json
import datetime
import operator

app = Flask(__name__)
app.secret_key ='mysecretkey'
riotAPIkey = "RGAPI-27c97ae6-7003-4a69-8ede-ac0d6cc073c6"
region = "na1"

championIDdict = {226: 'Aatrox', 103: 'Ahri', 84: 'Akali', 12: 'Alistar', 32: 'Amumu', 34: 'Anivia', 1: 'Annie',
523: 'Aphelios', 22: 'Ashe', 136: 'Aurelion Sol', 268: 'Azir', 432: 'Bard', 53: 'Blitzcrank', 63: 'Brand', 201: 'Braum',
51: 'Caitlyn', 164: 'Camille', 69: 'Cassiopeia', 31: 'Cho\'Gath', 42: 'Corki', 122: 'Darius', 131: 'Diana',
119: 'Draven', 245: 'Ekko', 60: 'Elise', 28: 'Evelynn', 81: 'Ezreal', 9: 'Fiddlesticks', 114: 'Fiora', 105: 'Fizz', 3: 'Galio',
41: 'Gangplank', 86: 'Garen', 150: 'Gnar', 79: 'Gragas', 104: 'Graves', 120: 'Hecarim', 74: 'Heimerdinger',
420: 'Illaoi', 39: 'Irelia', 427: 'Ivern', 40: 'Janna', 59: 'Jarvan IV', 24: 'Jax', 126: 'Jayce', 202: 'Jhin', 222: 'Jinx',
145: 'Kai\'Sa', 429: 'Kalista', 43: 'Karma', 30: 'Karthus', 38: 'Kassadin', 55: 'Katarina', 10: 'Kayle', 141: 'Kayn',
85: 'Kennen', 121: 'Kha\'Zix', 203: 'Kindred', 240: 'Kled', 96: 'Kog\'Maw', 7: 'LeBlanc', 64: 'Lee Sin', 89: 'Leona',
876: 'Lillia', 127: 'Lissandra', 236: 'Lucian', 117: 'Lulu', 99: 'Lux', 54: 'Malphite', 90: 'Malzahar', 57: 'Maokai',
11: 'Master Yi', 21: 'Miss Fortune', 62: 'Wukong', 82: 'Mordekaiser', 25: 'Morgana', 267: 'Nami', 75: 'Nasus',
111: 'Nautilus', 518: 'Neeko', 76: 'Nidalee', 56: 'Nocturne', 20: 'Nunu & Willump', 2: 'Olaf', 61: 'Orianna',
516: 'Ornn', 80: 'Pantheon', 78: 'Poppy', 555: 'Pyke', 246: 'Qiyana', 133: 'Quinn', 497: 'Rakan', 33: 'Rammus',
421: 'Rek\'Sai', 58: 'Renekton', 107: 'Rengar', 92: 'Riven', 68: 'Rumble', 13: 'Ryze', 360: 'Samira', 113: 'Sejuani',
235: 'Senna', 147: 'Seraphine', 875: 'Sett', 35: 'Shaco', 98: 'Shen', 102: 'Shyvana', 27: 'Singed', 14: 'Sion',
15: 'Sivir', 72: 'Skarner', 37: 'Sona', 16: 'Soraka', 50: 'Swain', 517: 'Sylas', 134: 'Syndra', 223: 'Tahm Kench',
163: 'Taliyah', 91: 'Talon', 44: 'Taric', 17: 'Teemo', 412: 'Thresh', 18: 'Tristana', 48: 'Trundle', 23: 'Tryndamere',
4: 'Twisted Fate', 29: 'Twitch', 77: 'Udyr', 6: 'Urgot', 110: 'Varus', 67: 'Vayne', 45: 'Veigar', 161: 'Vel\'Koz',
254: 'Vi', 112: 'Viktor', 8: 'Vladimir', 106: 'Volibear', 19: 'Warwick', 498: 'Xayah', 101: 'Xerath', 5: 'Xin Zhao', 
157: 'Yasuo', 777: 'Yone', 83: 'Yorick', 350: 'Yuumi', 154: 'Zac', 238: 'Zed', 115: 'Ziggs', 26: 'Zilean', 142: 'Zoe',
143: 'Zyra'}

summonerSpellIDdict = {21: 'Barrier', 1: 'Cleanse', 14: 'Ignite', 3: 'Exhaust', 4: 'Flash', 6: 'Ghost', 7: 'Heal',
13: 'Clarity', 30: 'To the King!', 31: 'Poro Toss', 11: 'Smite', 39: 'Mark', 32: 'Mark', 12: 'Teleport'}
















#displays the homepage to the user
@app.route('/')
def homepage():

	return render_template('Homepage.html')





@app.route('/SummonerSearch', methods = ['POST', 'GET'])
def summonerSearch():
	
	rows = []
	if request.method == 'POST':
		try:
			summonerName = request.form['Summoner']
			session['summonerName'] = summonerName
			setUpTempLast10GamesTable(summonerName)		
			profileIconID = session['profileIconID']  
			
			with sql.connect("LeagueOfData.db") as con:
				con.row_factory = sql.Row
				cur = con.cursor()
				cur.execute('''SELECT RecordOrRemove, GameID, GameMode, Champion, KDA, CS,
						Item0, Item1, Item2, Item3, Item4, Item5, Item6, Result
						FROM TempLast10Games''')
				rows = cur.fetchall()

		except:
			print("EXCEPTION BLOCK")
			con.rollback()
			

		finally:
			return render_template('SummonerSearch.html', rows = rows, summonerName = summonerName, profileIconID = profileIconID)

	if request.method == 'GET':
		try:	
			summonerName = session['summonerName']
			profileIconID = session['profileIconID']  
			setUpTempLast10GamesTable(summonerName)
			
			with sql.connect("LeagueOfData.db") as con:
				con.row_factory = sql.Row
				cur = con.cursor()
				cur.execute('''SELECT RecordOrRemove, GameID, GameMode, Champion, KDA, CS,
						Item0, Item1, Item2, Item3, Item4, Item5, Item6, Result
						FROM TempLast10Games''')
				rows = cur.fetchall()

		except:
			print("EXCEPTION BLOCK2")
			con.rollback()
			

		finally:
			return render_template('SummonerSearch.html', rows = rows, summonerName = summonerName, profileIconID = profileIconID)




@app.route('/entryAdded', methods = ['POST', 'GET'])
def entryAdded():
#This is the only page that makes inserts or deletes into the long term database(not the TempLast10Games table)
#it starts by checking if the gameID already exists in both tables. If it does not exisit, it means the user is trying
#to make an insert, which this page will do and inform the user of such. If it does exist, it means the user is trying
#to delete the games record from both tables, which this page will also do, and inform the user that it has been done.
	if request.method == 'POST':
		try:
			gameID = request.form['gameID']
			summonerName = session['summonerName']
			accountID = session['accountID']
			print(summonerName +"was playing in game #" + str(gameID) +" and has account id of " + accountID)
			with sql.connect("LeagueOfData.db") as con:
				cur = con.cursor()
				cur.execute(''' SELECT COUNT(1)
						FROM MatchList
						WHERE GameId = ? '''
						,(gameID,) )
				count = cur.fetchall()

			print(count[0])
			print(count[0][0])
			#this means the game does not currently exist in the table, and the user is trying to add it.	
			if count[0][0] == 0:
				#this is the part that inserts data to the MatchList table, which is a table that contains the
				#'high level' information so a user can easily identify a game	
				matchData = requestMatchData(region, gameID, riotAPIkey)
				queueID = matchData['queueId']
				queueName = getQueueNameFromQueueId(queueID)
				print(queueName)	
				for j in range(0,10):
					acctID = matchData['participantIdentities'][j]['player']['accountId'] 
					if accountID == acctID:
						participantID = matchData['participantIdentities'][j]['participantId']
						participantID = int(participantID)
				participantIndex = participantID - 1
				championID = matchData['participants'][participantIndex]['championId']
				championName = championIDdict[championID]
				print(championName)
				kills = matchData['participants'][participantIndex]['stats']['kills']
				deaths = matchData['participants'][participantIndex]['stats']['deaths']
				assists = matchData['participants'][participantIndex]['stats']['assists']
				kda = str(kills) + "/" + str(deaths) + "/" + str(assists)
				minions = matchData['participants'][participantIndex]['stats']['totalMinionsKilled']
				monsters = matchData['participants'][participantIndex]['stats']['neutralMinionsKilled']
				cs = minions + monsters
				print(kda + " cs:" + str(cs))
				item0 = matchData['participants'][participantIndex]['stats']['item0']
				item1 = matchData['participants'][participantIndex]['stats']['item1']
				item2 = matchData['participants'][participantIndex]['stats']['item2']
				item3 = matchData['participants'][participantIndex]['stats']['item3']
				item4 = matchData['participants'][participantIndex]['stats']['item4']
				item5 = matchData['participants'][participantIndex]['stats']['item5']
				item6 = matchData['participants'][participantIndex]['stats']['item6']
				teamID = matchData['participants'][participantIndex]['teamId']
				if teamID == 100:
					winOrLoss = matchData['teams'][0]['win']
				else:
					winOrLoss = matchData['teams'][1]['win']
				if winOrLoss == "Win":
					result = "Victory"
				else:
					result = "Defeat"
				print(result)
				timestamp = matchData['gameCreation']
				print(timestamp)
				timeOccurredUnix = timestamp/1000.0
				date = datetime.datetime.fromtimestamp(timeOccurredUnix)
				timeOccurred = date.strftime('%b-%d-%Y %H:%M:%S')
				print(timeOccurred)

			
				with sql.connect("LeagueOfData.db") as con:
					cur = con.cursor()
					cur.execute(''' INSERT INTO MatchList
					(AccountID, GameId, GameMode, Champion, KDA, CS,
					Item0, Item1, Item2, Item3, Item4, Item5, Item6, Result, TimeOccurred, TimeOccurredUnix)
					VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
					(accountID, gameID, queueName, championName, kda, cs,
					item0,item1,item2,item3,item4,item5,item6,result,timeOccurred,timeOccurredUnix) )
					con.commit()
				
				#this is the part that inserts data to the Match table, which is a table that contains the
				#'low level' details of games, so a user can do more in-depth analysis on a span of games
				spell1id = matchData['participants'][participantIndex]['spell1Id']
				spell2id = matchData['participants'][participantIndex]['spell2Id']
				spell1 = summonerSpellIDdict[spell1id]
				spell2 = summonerSpellIDdict[spell2id]
				print(spell1 + spell2)
				role = matchData['participants'][participantIndex]['timeline']['role']
				lane = matchData['participants'][participantIndex]['timeline']['lane']
				print(role + lane)
				opponentParticipantID = 0
				for j in range(0,10):
					opponentRole = matchData['participants'][j]['timeline']['role']
					opponentLane = matchData['participants'][j]['timeline']['lane']
					if lane == opponentLane and role == opponentRole and j != participantIndex:
						opponentParticipantID = matchData['participants'][j]['participantId']
						opponentParticipantID = int(opponentParticipantID)
				if opponentParticipantID != 0:		
					opponentParticipantIndex = opponentParticipantID - 1
					opponentChampionID = matchData['participants'][opponentParticipantIndex]['championId']
					opponentChampionName = championIDdict[opponentChampionID]
				else:
					opponentChampionName = "Undefined"
				print(opponentChampionName)

				largestKillingSpree = matchData['participants'][participantIndex]['stats']['largestKillingSpree']
				largestMultiKill = matchData['participants'][participantIndex]['stats']['largestMultiKill']
				killingSprees = matchData['participants'][participantIndex]['stats']['killingSprees']
				longestTimeSpentLiving = matchData['participants'][participantIndex]['stats']['longestTimeSpentLiving']
				doubleKills = matchData['participants'][participantIndex]['stats']['doubleKills']
				tripleKills = matchData['participants'][participantIndex]['stats']['tripleKills']
				quadraKills = matchData['participants'][participantIndex]['stats']['quadraKills']
				pentaKills = matchData['participants'][participantIndex]['stats']['pentaKills']
				unrealKills = matchData['participants'][participantIndex]['stats']['unrealKills']
				totalDamageDealt = matchData['participants'][participantIndex]['stats']['totalDamageDealt']
				magicDamageDealt = matchData['participants'][participantIndex]['stats']['magicDamageDealt']
				physicalDamageDealt = matchData['participants'][participantIndex]['stats']['physicalDamageDealt']
				trueDamageDealt = matchData['participants'][participantIndex]['stats']['trueDamageDealt']
				largestCriticalStrike = matchData['participants'][participantIndex]['stats']['largestCriticalStrike']
				totalDamageDealtToChampions = matchData['participants'][participantIndex]['stats']['totalDamageDealtToChampions']
				magicDamageDealtToChampions = matchData['participants'][participantIndex]['stats']['magicDamageDealtToChampions']
				physicalDamageDealtToChampions = matchData['participants'][participantIndex]['stats']['physicalDamageDealtToChampions']
				trueDamageDealtToChampions = matchData['participants'][participantIndex]['stats']['trueDamageDealtToChampions']
				totalHeal = matchData['participants'][participantIndex]['stats']['totalHeal']
				totalUnitsHealed = matchData['participants'][participantIndex]['stats']['totalUnitsHealed']
				damageSelfMitigated = matchData['participants'][participantIndex]['stats']['damageSelfMitigated']
				damageDealtToObjectives = matchData['participants'][participantIndex]['stats']['damageDealtToObjectives']
				damageDealtToTurrets = matchData['participants'][participantIndex]['stats']['damageDealtToTurrets']
				visionScore = matchData['participants'][participantIndex]['stats']['visionScore']
				timeCCingOthers = matchData['participants'][participantIndex]['stats']['timeCCingOthers']
				totalDamageTaken = matchData['participants'][participantIndex]['stats']['totalDamageTaken']
				magicalDamageTaken = matchData['participants'][participantIndex]['stats']['magicalDamageTaken']
				physicalDamageTaken = matchData['participants'][participantIndex]['stats']['physicalDamageTaken']
				trueDamageTaken = matchData['participants'][participantIndex]['stats']['trueDamageTaken']
				goldEarned = matchData['participants'][participantIndex]['stats']['goldEarned']
				goldSpent = matchData['participants'][participantIndex]['stats']['goldSpent']
				print(goldSpent)
				turretKills = matchData['participants'][participantIndex]['stats']['turretKills']
				inhibitorKills = matchData['participants'][participantIndex]['stats']['inhibitorKills']
				totalMinionsKilled = matchData['participants'][participantIndex]['stats']['totalMinionsKilled']
				neutralMinionsKilled = matchData['participants'][participantIndex]['stats']['neutralMinionsKilled']
				neutralMinionsKilledTeamJungle = 0 #these variables are set to 0 beforehand in the case of gamemodes
				neutralMinionsKilledEnemyJungle = 0 #that do not have jungles and don't return this variable from the api
				wardsPlaced = 0 
				wardsKilled = 0
				if queueID != 450 and queueID != 920:
					neutralMinionsKilledTeamJungle = matchData['participants'][participantIndex]['stats']['neutralMinionsKilledTeamJungle']
					neutralMinionsKilledEnemyJungle = matchData['participants'][participantIndex]['stats']['neutralMinionsKilledEnemyJungle']
					wardsPlaced = matchData['participants'][participantIndex]['stats']['wardsPlaced']
					wardsKilled = matchData['participants'][participantIndex]['stats']['wardsKilled']
				totalTimeCrowdControlDealt = matchData['participants'][participantIndex]['stats']['totalTimeCrowdControlDealt']
				champLevel = matchData['participants'][participantIndex]['stats']['champLevel']
				print(champLevel)
				visionWardsBoughtInGame = matchData['participants'][participantIndex]['stats']['visionWardsBoughtInGame']
				sightWardsBoughtInGame = matchData['participants'][participantIndex]['stats']['sightWardsBoughtInGame']
				firstBloodKill = matchData['participants'][participantIndex]['stats']['firstBloodKill']
				firstBloodAssist = matchData['participants'][participantIndex]['stats']['firstBloodAssist']
				firstTowerKill = False
				firstTowerAssist = False
				firstInhibitorKill = False
				firstInhibitorAssist = False
				if turretKills > 0:
					firstTowerKill = matchData['participants'][participantIndex]['stats']['firstTowerKill']
					firstTowerAssist = matchData['participants'][participantIndex]['stats']['firstTowerAssist']
				if inhibitorKills > 0:
					firstInhibitorKill = matchData['participants'][participantIndex]['stats']['firstInhibitorKill']
					firstInhibitorAssist = matchData['participants'][participantIndex]['stats']['firstInhibitorAssist']
				combatPlayerScore = matchData['participants'][participantIndex]['stats']['combatPlayerScore']
				objectivePlayerScore = matchData['participants'][participantIndex]['stats']['objectivePlayerScore']
				totalPlayerScore = matchData['participants'][participantIndex]['stats']['totalPlayerScore']
				totalScoreRank = matchData['participants'][participantIndex]['stats']['totalScoreRank']

				
				with sql.connect("LeagueOfData.db") as con:
					cur = con.cursor()
					cur.execute(''' INSERT INTO Match
					(AccountID,GameId,ParticipantID,TeamID,Champion,Spell1,Spell2,
					Kills,Deaths,Assists,Result,
					Role,Lane,OpponentChampion,largestKillingSpree,largestMultiKill,killingSprees,longestTimeSpentLiving,
					doubleKills,tripleKills,quadraKills,pentaKills,unrealKills,totalDamageDealt,magicDamageDealt,
					physicalDamageDealt,trueDamageDealt,largestCriticalStrike,totalDamageDealtToChampions,magicDamageDealtToChampions,
					physicalDamageDealtToChampions,trueDamageDealtToChampions,totalHeal,totalUnitsHealed,damageSelfMitigated,
					damageDealtToObjectives,damageDealtToTurrets,visionScore,timeCCingOthers,totalDamageTaken,magicalDamageTaken,
					physicalDamageTaken,trueDamageTaken,goldEarned,goldSpent,turretKills,inhibitorKills,totalMinionsKilled,
					neutralMinionsKilled,neutralMinionsKilledTeamJungle,neutralMinionsKilledEnemyJungle,totalTimeCrowdControlDealt,
					champLevel,visionWardsBoughtInGame,sightWardsBoughtInGame,wardsPlaced,wardsKilled,firstBloodKill,firstBloodAssist,
					firstTowerKill,firstTowerAssist,firstInhibitorKill,firstInhibitorAssist,combatPlayerScore,objectivePlayerScore,
					totalPlayerScore,totalScoreRank
					)
					VALUES (?,?,?,?,?,?,?,
					?,?,?,?,
					?,?,?,?,?,?,?,
					?,?,?,?,?,?,?,
					?,?,?,?,?,
					?,?,?,?,?,
					?,?,?,?,?,?,
					?,?,?,?,?,?,?,
					?,?,?,?,
					?,?,?,?,?,?,?,
					?,?,?,?,?,?,
					?,?
					)''',
					(accountID,gameID,participantID,teamID,championName,spell1,spell2,
					kills,deaths,assists,result,
					role,lane,opponentChampionName,largestKillingSpree,largestMultiKill,killingSprees,longestTimeSpentLiving,
					doubleKills,tripleKills,quadraKills,pentaKills,unrealKills,totalDamageDealt,magicDamageDealt,
					physicalDamageDealt,trueDamageDealt,largestCriticalStrike,totalDamageDealtToChampions,magicDamageDealtToChampions,
					physicalDamageDealtToChampions,trueDamageDealtToChampions,totalHeal,totalUnitsHealed,damageSelfMitigated,
					damageDealtToObjectives,damageDealtToTurrets,visionScore,timeCCingOthers,totalDamageTaken,magicalDamageTaken,
					physicalDamageTaken,trueDamageTaken,goldEarned,goldSpent,turretKills,inhibitorKills,totalMinionsKilled,
					neutralMinionsKilled,neutralMinionsKilledTeamJungle,neutralMinionsKilledEnemyJungle,totalTimeCrowdControlDealt,
					champLevel,visionWardsBoughtInGame,sightWardsBoughtInGame,wardsPlaced,wardsKilled,firstBloodKill,firstBloodAssist,
					firstTowerKill,firstTowerAssist,firstInhibitorKill,firstInhibitorAssist,combatPlayerScore,objectivePlayerScore,
					totalPlayerScore,totalScoreRank) )
					con.commit()

				msg = summonerName + "\'s " + championName + " game on " + timeOccurred + " was recorded succcessfully!"

			#this is if the count is not 0, then the user is trying to remove an entry from the table
			else:
				print("about to delete")
				with sql.connect("LeagueOfData.db") as con:
					cur = con.cursor()
					cur.execute('DELETE FROM MatchList WHERE GameId = ?', (gameID,) )
					con.commit()
					cur.execute('DELETE FROM Match WHERE GameId = ?', (gameID,) )
					con.commit()

				print("deleted")
				msg = summonerName + "\'s game successfully removed from the database!"
		except:
			print("EXCEPTION BLOCK")
			msg = "Error recording game for " + summonerName + "!"

		finally:
			return render_template('entryAdded.html', msg = msg, summonerName = summonerName)




@app.route('/recordedGames', methods = ['POST', 'GET'])
def recordedGames():
	
	if request.method == 'POST' or request.method == 'GET':
		try:
	
			summonerName = session['summonerName']
			accountID = session['accountID']
			profileIconID = session['profileIconID']

			with sql.connect("LeagueOfData.db") as con:
				con.row_factory = sql.Row
				cur = con.cursor()
				cur.execute('''SELECT GameId, GameMode, Champion, KDA, CS,
						Item0, Item1, Item2, Item3, Item4, Item5, Item6, Result, TimeOccurred
						FROM MatchList
						WHERE AccountID = ?
						ORDER BY TimeOccurredUnix DESC'''
						,(accountID,) )
				rows = cur.fetchall()






		except:
			print('EXCEPTION BLOCK')
			con.rollback()
	
		finally:
			return render_template('recordedGames.html', rows = rows, profileIconID = profileIconID, summonerName = summonerName)



@app.route('/viewStats', methods = ['POST', 'GET'])
def viewStats():

	return render_template('viewStats.html')

@app.route('/gameDetails', methods = ['POST', 'GET'])
def gameDetails():
	
	if request.method == 'POST':
		try:
			gameID = request.form['gameID']
			summonerName = session['summonerName']
			with sql.connect("LeagueOfData.db") as con:
				con.row_factory = sql.Row
				cur = con.cursor()

				cur.execute('''SELECT *
                                            FROM  MatchList
                                            INNER JOIN Match
                                            ON MatchList.GameId = Match.GameId
                                            WHERE MatchList.GameId = ?'''
                                            ,(gameID, ) )
				rows = cur.fetchall()
			
			session['champion'] = rows[0]['Champion']
			if rows[0]['lane'] == 'JUNGLE':
				lane = "Jungle"
			elif rows[0]['lane'] == 'TOP':
				lane = "Top"
			elif rows[0]['lane'] == 'MIDDLE':
				lane = "Mid"
			elif rows[0]['lane'] == 'BOTTOM' and rows[0]['role'] == 'DUO_CARRY':
				lane = "ADC"
			else:
				lane = "Support"

		except:
			print('EXCEPTION BLOCK')
			con.rollback()

		finally:
			return render_template('gameDetails.html', rows = rows, lane = lane, summonerName=summonerName)



@app.route('/updateMatchup', methods = ['POST', 'GET'])
def updateMatchup():


	if request.method == 'POST':
		try:
			gameID = request.form['gameID']
			session['gameID'] = gameID
			accountID = session['accountID']
			matchData = requestMatchData(region, gameID, riotAPIkey)
			with sql.connect("LeagueOfData.db") as con:
				con.row_factory = sql.Row
				cur = con.cursor()
				cur.execute('''SELECT TeamID
						FROM Match
						WHERE AccountID = ? AND GameId = ?'''
                                                ,(accountID, gameID,) )
				row = cur.fetchall()

			teamID = row[0]['TeamID']
			opponentList = []


			if teamID != 100:
				opponentList.append(matchData['participants'][0]['championId'])
				opponentList.append(matchData['participants'][1]['championId'])
				opponentList.append(matchData['participants'][2]['championId'])
				opponentList.append(matchData['participants'][3]['championId'])
				opponentList.append(matchData['participants'][4]['championId'])
			else:
				opponentList.append(matchData['participants'][5]['championId'])
				opponentList.append(matchData['participants'][6]['championId'])
				opponentList.append(matchData['participants'][7]['championId'])
				opponentList.append(matchData['participants'][8]['championId'])
				opponentList.append(matchData['participants'][9]['championId'])
			print(str(opponentList[0])+ " " +str(opponentList[1])+ " " +str(opponentList[2])+ " " +str(opponentList[3])+ " " +str(opponentList[4]))

			opponentChampions = []
			for i in range(0,len(opponentList)):
				opponentChampions.append(championIDdict[opponentList[i]])

			print(str(opponentChampions[0])+ " " +str(opponentChampions[1])+ " " +str(opponentChamions[2])+ " " +str(opponentChampions[3])+ " " +str(opponentChampions[4]))
		finally:
			return render_template('updateMatchup.html', opponentChampions = opponentChampions)


@app.route('/championData', methods = ['POST', 'GET'])
def championData():

	if request.method == 'POST':
		try:
			with sql.connect("LeagueOfData.db") as con:
				con.row_factory = sql.Row
				cur = con.cursor()
				cur.execute('''SELECT DISTINCT Champion
						FROM MatchList
						ORDER BY Champion ASC''')
				rows = cur.fetchall()
				
		except:
			print('EXCEPTION BLOCK')
		finally:
			return render_template('championData.html', rows = rows, len = len(rows))


@app.route('/championDetails', methods = ['POST', 'GET'])
def championDetails():

	if request.method == 'POST':
		try:
			champion = session['champion'] 

			print('i am here!')
			with sql.connect("LeagueOfData.db") as con:
				con.row_factory = sql.Row
				cur = con.cursor()
				cur.execute('''SELECT ROUND(AVG(Kills), 3) as Kills,
                                                    ROUND(AVG(Deaths), 3) as Deaths,ROUND(AVG(Assists), 3) as Assists,
                                                    ROUND(AVG(totalMinionsKilled), 3) as totalMinionsKilled,ROUND(AVG(neutralMinionsKilled), 3) as neutralMinionsKilled,
                                                    ROUND(AVG(champLevel), 3) as champLevel,ROUND(AVG(goldEarned), 3) as goldEarned,
                                                    ROUND(AVG(damageDealtToObjectives), 3) as damageDealtToObjectives,ROUND(AVG(damageDealtToTurrets), 3) as damageDealtToTurrets,
                                                    ROUND(AVG(TurretKills), 3) as TurretKills,ROUND(AVG(inhibitorKills), 3) as inhibitorKills,
                                                    ROUND(AVG(neutralMinionsKilledEnemyJungle), 3) as neutralMinionsKilledEnemyJungle,ROUND(AVG(visionScore), 3) as visionScore,
                                                    ROUND(AVG(wardsPlaced), 3) as wardsPlaced,ROUND(AVG(wardsKilled), 3) as wardsKilled,
                                                    ROUND(AVG(visionWardsBoughtInGame), 3) as visionWardsBoughtInGame,ROUND(AVG(totalDamageDealt), 3) as totalDamageDealt,
                                                    ROUND(AVG(physicalDamageDealt), 3) as physicalDamageDealt,ROUND(AVG(magicDamageDealt), 3) as magicDamageDealt,
                                                    ROUND(AVG(trueDamageDealt), 3) as trueDamageDealt,ROUND(AVG(totalDamageDealtToChampions), 3) as totalDamageDealtToChampions,
                                                    ROUND(AVG(physicalDamageDealtToChampions), 3) as physicalDamageDealtToChampions,ROUND(AVG(magicDamageDealtToChampions), 3) as magicDamageDealtToChampions,
                                                    ROUND(AVG(trueDamageDealtToChampions), 3) as trueDamageDealtToChampions,ROUND(AVG(totalDamageTaken), 3) as totalDamageTaken,
                                                    ROUND(AVG(physicalDamageTaken), 3) as physicalDamageTaken,ROUND(AVG(magicalDamageTaken), 3) as magicalDamageTaken,
                                                    ROUND(AVG(trueDamageTaken), 3) as trueDamageTaken,ROUND(AVG(totalHeal), 3) as totalHeal,
                                                    ROUND(AVG(timeCCingOthers), 3) as timeCCingOthers,ROUND(AVG(doubleKills), 3) as doubleKills,
                                                    ROUND(AVG(tripleKills), 3) as tripleKills,ROUND(AVG(quadraKills), 3) as quadraKills,
                                                    ROUND(AVG(pentaKills), 3) as pentaKills,ROUND(AVG(largestKillingSpree), 3) as largestKillingSpree
                                            FROM  Match
                                            WHERE Champion = ?'''
                                            ,(champion, ) )
				rows = cur.fetchall()

			with sql.connect("LeagueOfData.db") as con:
				con.row_factory = sql.Row
				cur = con.cursor()
				cur.execute('''SELECT SummonerName,
                                            ROUND(AVG(goldEarned), 3) as goldEarned
                                            FROM  SuperTable
                                            WHERE Champion = ?
                                            GROUP BY SummonerName
                                            ORDER BY goldEarned DESC'''
                                            ,(champion, ) )
				gold = cur.fetchall()
			with sql.connect("LeagueOfData.db") as con:
				con.row_factory = sql.Row
				cur = con.cursor()
				cur.execute('''SELECT SummonerName,
                                            ROUND(AVG(damageDealtToObjectives), 3) as damageDealtToObjectives
                                            FROM  SuperTable
                                            WHERE Champion = ?
                                            GROUP BY SummonerName
                                            ORDER BY damageDealtToObjectives DESC'''
                                            ,(champion, ) )
				dObj = cur.fetchall()
			with sql.connect("LeagueOfData.db") as con:
				con.row_factory = sql.Row
				cur = con.cursor()
				cur.execute('''SELECT SummonerName,
                                            ROUND(AVG(totalDamageDealtToChampions), 3) as totalDamageDealtToChampions
                                            FROM  SuperTable
                                            WHERE Champion = ?
                                            GROUP BY SummonerName
                                            ORDER BY totalDamageDealtToChampions DESC'''
                                            ,(champion, ) )
				dCham = cur.fetchall()
			with sql.connect("LeagueOfData.db") as con:
				con.row_factory = sql.Row
				cur = con.cursor()
				cur.execute('''SELECT SummonerName,
                                            ROUND(AVG(timeCCingOthers), 3) as timeCCingOthers
                                            FROM  SuperTable
                                            WHERE Champion = ?
                                            GROUP BY SummonerName
                                            ORDER BY timeCCingOthers DESC'''
                                            ,(champion, ) )
				cc = cur.fetchall()
			bestPlayers = {}
			mostGold = {}
			mostDobj = {}
			mostDchamp = {}
			mostCC = {}
			for i in range(0, len(gold)):
				mostGold[gold[i]['SummonerName']] = len(gold) - i
				bestPlayers[gold[i]['SummonerName']] = 0
				print(gold[i]['SummonerName'] + str(len(gold)-i))

			for i in range(0, len(dObj)):
				mostDobj[dObj[i]['SummonerName']] = len(dObj) - i
				bestPlayers[dObj[i]['SummonerName']] = 0
				print(dObj[i]['SummonerName'] + str(len(dObj)-i))


			for i in range(0, len(dCham)):
				mostDchamp[dCham[i]['SummonerName']] = len(dCham) - i
				bestPlayers[dCham[i]['SummonerName']] = 0
				print(dCham[i]['SummonerName'] + str(len(dCham)-i))

			for i in range(0, len(cc)):
				mostCC[cc[i]['SummonerName']] = len(cc) - i
				bestPlayers[cc[i]['SummonerName']] = 0
				print(cc[i]['SummonerName'] + str(len(cc)-i))

			for key in bestPlayers:
				bestPlayers[key] = mostGold[key] + mostDobj[key] + mostDchamp[key] + mostCC[key]
				print( key + str(bestPlayers[key]))

			bestPlayerList = sorted(bestPlayers.items(), key = lambda x: x[1], reverse=True)
			print("it worked")
			bestPlayerIcon = []
			if len(bestPlayerList) < 5:
				maxRange = len(bestPlayerList)
			else:
				maxRange = 5
			for i in range(0,maxRange): 
				sumData = requestSummonerData(region,bestPlayerList[i][0],riotAPIkey)
				bestPlayerIcon.append(sumData['profileIconId'])






		except:
			print('EXCEPTION BLOCK3')
		finally:
			return render_template('championDetails.html', rows = rows, champion = champion,bestPlayers = bestPlayerList, bestPlayerIcon = bestPlayerIcon,maxRange = maxRange)

@app.route('/updatedMatchup', methods = ['POST', 'GET'])
def updatedMatchup():

	if request.method == 'POST':
		try:
			opponentChampion = request.form['ch']
			print(opponentChampion)
			gameID = session['gameID']
			accountID = session['accountID']
			summonerName = session['summonerName']
			with sql.connect("LeagueOfData.db") as con:
				cur = con.cursor()
				cur.execute('''UPDATE Match 
                                                SET OpponentChampion = ?
						WHERE GameId = ? and AccountID = ?'''
                                                ,(opponentChampion,gameID, accountID,) )
				con.commit()
				msg = 'Matchup updated Successfully!'
		except:
			print('EXCEPTION BLOCK')
			msg = 'Error in updating matchup!'
		finally:
			return render_template('updatedMatchup.html', msg = msg, summonerName = summonerName)


def requestSummonerData(region, summonerName, APIkey):
	URL = "https://" + region + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summonerName + "?api_key=" + APIkey
	print(URL)
	response = requests.get(URL)
	return response.json()



def requestMatchListData(region, accountId, APIkey):
	URL = "https://" + region + ".api.riotgames.com/lol/match/v4/matchlists/by-account/" + accountId + "?api_key=" + APIkey
	print(URL)
	response = requests.get(URL)
	return response.json()

def requestMatchData(region, gameId, APIkey):
	URL = "https://" + region + ".api.riotgames.com/lol/match/v4/matches/" + str(gameId) + "?api_key=" + APIkey
	print(URL)
	response = requests.get(URL)
	return response.json()



def getQueueNameFromQueueId(queueId):
	with open('jsons/queues.json', 'r') as queueFile:
		queueDataResponse = queueFile.read()
		queueData = json.loads(queueDataResponse)
		queueName = "error! error!"
		for x in range(0,len(queueData)):
			toCompare = queueData[x]['queueId']
			if toCompare == queueId:
				queueName = queueData[x]['description']
		queueName = queueName[0:-6]

	return queueName




def setUpTempLast10GamesTable(summonerName):
			with sql.connect("LeagueOfData.db") as con:
				cur = con.cursor()
				cur.execute('DELETE FROM TempLast10Games')
				con.commit()

			summonerDataResponse = requestSummonerData(region, summonerName, riotAPIkey)
			accountID = summonerDataResponse['accountId']
			with sql.connect("LeagueOfData.db") as con:
				cur = con.cursor()
				cur.execute(''' INSERT OR IGNORE INTO Summoner
				(SummonerName, AccountID)
				VALUES (?,?)''',
				(summonerName, accountID))	
				con.commit()
			session['accountID'] = accountID
			profileIconID = summonerDataResponse['profileIconId']
			profileIconID = str(profileIconID)
			session['profileIconID'] = profileIconID
			accountID = str(accountID)

			print(accountID)			
			print(profileIconID)			

			matchListDataResponse = requestMatchListData(region, accountID, riotAPIkey)
		
			participantID = 0
			for i in range(0,10):
				gameID = matchListDataResponse['matches'][i]['gameId']
				gameID = int(gameID)
				print(gameID)
				with sql.connect("LeagueOfData.db") as con:
					cur = con.cursor()
					cur.execute(''' SELECT COUNT(1)
							FROM MatchList
							WHERE GameId = ? '''
							,(gameID,) )
					count = cur.fetchall()
				if count[0][0] == 0:
					recordOrRemove = "Record"
				else:
					recordOrRemove = "Remove"
				
				matchData = requestMatchData(region, gameID, riotAPIkey)
				for j in range(0,10):
					acctID = matchData['participantIdentities'][j]['player']['accountId'] 
					acctID = str(acctID)
					if accountID == acctID:
						participantID = matchData['participantIdentities'][j]['participantId']
						print(acctID)
						participantID = int(participantID)
						print(participantID)
				participantIndex = participantID - 1
				championID = matchData['participants'][participantIndex]['championId']
				championName = championIDdict[championID]	
				kills = matchData['participants'][participantIndex]['stats']['kills']
				deaths = matchData['participants'][participantIndex]['stats']['deaths']
				assists = matchData['participants'][participantIndex]['stats']['assists']
				kda = str(kills) + "/" + str(deaths) + "/" + str(assists)	
				print(summonerName + " was playing " + str(championName) + " and had a K/D/A of " + kda )
				gameTypeID = matchData['queueId']
				queueName = getQueueNameFromQueueId(gameTypeID)
				print(queueName)

				#queueFile.close()
				minions = matchData['participants'][participantIndex]['stats']['totalMinionsKilled']
				monsters = matchData['participants'][participantIndex]['stats']['neutralMinionsKilled']
				cs = minions + monsters		
				item0 = matchData['participants'][participantIndex]['stats']['item0']
				item1 = matchData['participants'][participantIndex]['stats']['item1']
				item2 = matchData['participants'][participantIndex]['stats']['item2']
				item3 = matchData['participants'][participantIndex]['stats']['item3']
				item4 = matchData['participants'][participantIndex]['stats']['item4']
				item5 = matchData['participants'][participantIndex]['stats']['item5']
				item6 = matchData['participants'][participantIndex]['stats']['item6']
				teamID = matchData['participants'][participantIndex]['teamId']
				if teamID == 100:
					winOrLoss = matchData['teams'][0]['win']
				else:
					winOrLoss = matchData['teams'][1]['win']
				
				if winOrLoss == "Win":
					result = "Victory"
				else:
					result = "Defeat"
				print(summonerName + " was in a " + str(queueName) + " game and had  " + str(cs) + " cs with a result of a " + str(result) )
				with sql.connect("LeagueOfData.db") as con:
					cur = con.cursor()
					cur.execute(''' INSERT INTO TempLast10Games
					(RecordOrRemove,GameId,GameMode,Champion,KDA,CS,Item0,Item1,Item2,Item3,Item4,Item5,Item6,Result)
					VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
					(recordOrRemove,gameID,queueName,championName,kda,cs,item0,item1,item2,item3,item4,item5,item6,result))	
					con.commit()





if __name__ == '__main__':
	app.run()
