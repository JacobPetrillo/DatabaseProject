'''
Jacob Petrillo
Fall 2020
COP4710
'''
import sqlite3 as sql

conn = sql.connect("LeagueOfData.db")
print("Opened database successfully")

conn.execute('''CREATE TABLE TempLast10Games
		(
		RecordOrRemove TEXT(6),
		GameId INT,
		GameMode TEXT(35),
		Champion TEXT(20),
		KDA TEXT(10),
		CS INT,
		Item0 INT,
		Item1 INT,
		Item2 INT,
		Item3 INT,
		Item4 INT,
		Item5 INT,
		Item6 INT,
		Result TEXT(7)
		)''')
print("Temporary Last 10 Games table created successfully")

conn.execute('''CREATE TABLE Summoner
                (
                AccountID TEXT(56),
                SummonerName TEXT(16),
                UNIQUE(AccountID)
                )''')
print("summoner table created successfully")

conn.execute('''CREATE TABLE MatchList
		(
		AccountID TEXT(56),
		GameId INT,
		GameMode TEXT(35),
		Champion TEXT(20),
		KDA TEXT(10),
		CS INT,
		Item0 INT,
		Item1 INT,
		Item2 INT,
		Item3 INT,
		Item4 INT,
		Item5 INT,
		Item6 INT,
		Result TEXT(7),
		TimeOccurred TEXT(25),
		TimeOccurredUnix INT
		)''')
print("MatchList table created successfully")

conn.execute('''CREATE TABLE Match
		(
		AccountID TEXT(56),
		GameId INT,
		ParticipantID INT,
		TeamID INT,
		Champion TEXT(20),
		Spell1 TEXT(30),
		Spell2 TEXT(30),
		Kills INT,	
		Deaths INT,
		Assists INT,
                Result TEXT(7),
		Role TEXT(11),
		Lane Text(6),
		OpponentChampion TEXT(20),
		largestKillingSpree INT,
		largestMultiKill INT,
		killingSprees INT,
		longestTimeSpentLiving INT,
		doubleKills INT,
		tripleKills INT,
		quadraKills INT,
		pentaKills INT,
		unrealKills INT,
		totalDamageDealt INT,
		magicDamageDealt INT,
		physicalDamageDealt INT,
		trueDamageDealt INT,
		largestCriticalStrike INT,
		totalDamageDealtToChampions INT,
		magicDamageDealtToChampions INT,
		physicalDamageDealtToChampions INT,
		trueDamageDealtToChampions INT,
		totalHeal INT,
		totalUnitsHealed INT,
		damageSelfMitigated INT,
		damageDealtToObjectives INT,
		damageDealtToTurrets INT,
		visionScore INT,
		timeCCingOthers INT,
		totalDamageTaken INT,
		magicalDamageTaken INT,
		physicalDamageTaken INT,
		trueDamageTaken INT,
		goldEarned INT,
		goldSpent INT,
		turretKills INT,
		inhibitorKills INT,
		totalMinionsKilled INT,
		neutralMinionsKilled INT,
		neutralMinionsKilledTeamJungle INT,
		neutralMinionsKilledEnemyJungle INT,
		totalTimeCrowdControlDealt INT,
		champLevel INT,
		visionWardsBoughtInGame INT,
		sightWardsBoughtInGame INT,
		wardsPlaced INT,
		wardsKilled INT,
		firstBloodKill BOOL,
		firstBloodAssist BOOL,
		firstTowerKill BOOL,
		firstTowerAssist BOOL,
		firstInhibitorKill BOOL, 
		firstInhibitorAssist BOOL, 
		combatPlayerScore INT, 
		objectivePlayerScore INT,
		totalPlayerScore INT,
		totalScoreRank INT
		)''')


print("Match table created successfully")
 

conn.execute('''CREATE VIEW SuperTable
                AS
                SELECT *
                FROM Summoner
                INNER JOIN MatchList ON Summoner.AccountID = MatchList.AccountID
                INNER JOIN Match ON Summoner.AccountID = Match.AccountID
                ''')
print("SuperTable View created successfully")








