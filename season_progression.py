#functions
def open_save():
	with open('savedata.sav','rb') as game_data:
		in_data = game_data.read()

	decomp = zlib.decompress(in_data)
	f = open('database.sqlite','wb')
	f.write(decomp)
	f.close()

def teardown():
	conn.close()
	os.remove('database.sqlite')
	sys.exit(0)

def create_player():
	stats = [1]
	skill = 0
	while(sum(stats)<215 or max(stats)<55 or sum(stats)>300):
		stats = []
		for i in range(0,5):
			if(random()>.8):
				skill = 10+20*random()+20*random()+40*random()
			else:
				skill = 10+60*random()
				
			stats += [round(skill),]
	stats += [0,0,0]
	return stats

def create_pitcher():
	stats = [1]
	skill = 0
	while(sum(stats)<240 or max(stats)<55 or sum(stats)>330):
		stats = []
		for i in range(0,4):
			if(random()>.9):
				skill = 5+25*random()+20*random()+20*random()
			else:
				if(i<3):
					skill = 15*random()+15*random()
				else:
					skill = 10+50*random()+10*random()
			stats+= [round(skill),]
		for i in range(0,4):
			if(random()>.85):
				skill = 15+30*random()+20*random()+20*random()
			else:
				skill = 10+50*random()+10*random()
			stats+= [round(skill),]
	return stats

def random_pitches(role):
	pitch_types = []
	if(role=='SP'):
		num_pitches = int(4+1.2*random())
	elif(role=='RP'):
		num_pitches = int(3+1.2*random())
	else:
		num_pitches = int(2+1.2*random())
	
	if(random()<0.96):
		pitch_types += [1,]
		num_pitches -=1
	for i in range(0,num_pitches):
		done = False
		while(not done):
			new_pitch = randint(1,8)
			unique = True
			for j in range(0,len(pitch_types)):
				if(new_pitch==pitch_types[j]):
					unique = False
			if(unique):
				done=True
		pitch_types += [new_pitch,]

	return pitch_types

def gen_gender_po(id, gender):
	temp = []
	if(gender==1):
		pass
		temp += ((id, 0, 1, 0),)
		temp += ((id, 12, randint(0,4), 0),)
		temp += ((id, 14, randint(0,3), 0),)
		temp += ((id, 15, randint(1,6), 0),)
		temp += ((id, 16, 0, 0),)
		temp += ((id, 22, randint(0,1), 0),)			
	else:
		temp += ((id, 0, 0, 0),)
		temp += ((id, 12, randint(0,9), 0),)
		temp += ((id, 14, randint(0,2), 0),)
		temp += ((id, 15, randint(0,15), 0),)
		if(random()>.8):
			temp += ((id, 16, randint(0,28), 0),)
		else:
			temp += ((id, 16, 0, 0),)
		temp += ((id, 22, randint(2,4), 0),)
	return temp

def gen_generic_po(id):
	temp = []
	temp += ((id, 4, randint(0,1), 0),)
	if(random()>.8):
		temp += ((id, 5, 2, 0),)
	else:
		temp += ((id, 5, randint(0,1), 0),)
	temp += ((id, 8, randint(0,6), 0),)
	if(random()>.90):
		temp += ((id, 17, randint(1,4), 0),)
	else:
		temp += ((id, 17, 0, 0),)
	temp += ((id, 18, randint(0,1), 0),)
	if(random()>.85):
		temp += ((id, 19, randint(0,7), 0),)
	else:
		temp += ((id, 19, 0, 0),)
	temp += ((id, 20, randint(0,98), 0),)
	temp += ((id, 25, randint(0,1), 0),)
	temp += ((id, 26, randint(0,1), 0),)
	temp += ((id, 27, randint(1,4), 0),)
	if(random()>.9):
		temp += ((id, 28, randint(1,5), 0),)
	else:
		temp += ((id, 28, 0, 0),)
	if(random()>.9):
		temp += ((id, 29, randint(1,5), 0),)
	else:
		temp += ((id, 29, 0, 0),)
	temp += ((id, 30, randint(0,3), 0),)
	temp += ((id, 31, randint(0,3), 0),)
	temp += ((id, 32, randint(0,3), 0),)
	temp += ((id, 36, randint(0,3), 0),)
	temp += ((id, 39, randint(0,2), 0),)
	temp += ((id, 40, randint(0,2), 0),)
	temp += ((id, 41, randint(0,8), 0),)
	temp += ((id, 50, randint(0,14), 0),)
	temp += ((id, 51, randint(0,17), 5),)
	temp += ((id, 52, randint(0,75), 5),)
	temp += ((id, 92, randint(0,4), 0),)
	temp += ((id, 93, randint(0,3), 0),)
	temp += ((id, 104, 0, 0),)
	return temp
	
import zlib
import sqlite3
import os
import sys
import male_n
import female_n
import last_n
from random import randint,random,choice

os.system('mode 140,40')
male_names = male_n.male_first_names()	
female_names = female_n.female_first_names()	
last_names = last_n.last_names()	

try:
	open_save()
except:
	print("Save file not found.  Enter to Exit")
	input()
	sys.exit(0)


conn = sqlite3.connect('database.sqlite')
c = conn.cursor()


c.execute('SELECT * FROM t_seasons WHERE completionDate is null and elimination = 0')
seasons_incomplete = c.fetchall()
    
#select which season
for i in range(0,len(seasons_incomplete)):
	seasonteams =[]
	c.execute('SELECT DISTINCT homeTeamGUID FROM t_season_schedule WHERE seasonGUID = ?',(seasons_incomplete[i][0],))
	seasonteams_id = c.fetchall()
	print("Season with teams:\n")
	for team in range(0,len(seasonteams_id)):
		c.execute('SELECT * FROM t_teams WHERE GUID = ?',seasonteams_id[team])
		seasonteams += (c.fetchall()[0],)
		print(seasonteams[team][2])
	decision = input("\nIs this the season to update? (1) for yes (2) for no:")
	while(decision.strip() != '1' and decision.strip() != '2'):
		decision = input('\nNot a valid option. 1 or 2')
	if(decision.strip()=='1'):
		season = i
		break
	else:
		season = -1

if(season == -1):
	print("\nNo suitable seasons found.  Press enter to close")
	input()
	teardown()
		
#recover unique team IDs from season schedule    
c.execute('SELECT DISTINCT homeTeamGUID FROM t_season_schedule WHERE seasonGUID = ?',(seasons_incomplete[season][0],))
teams = c.fetchall()


teamorig_guid = []
players_to_write = []
original_teams = []
custom_teams = []
#recover player information, team data, and original team guid from the unique team IDs
for team in range(0,len(teams)):
	c.execute('SELECT * FROM t_baseball_players WHERE teamGUID = ?',teams[team])
	players_to_write += (c.fetchall(),)
	c.execute('SELECT * FROM t_teams WHERE GUID = ?',teams[team])
	custom_teams += (c.fetchall()[0],)
	c.execute('SELECT originalGUID FROM t_teams WHERE GUID = ?',teams[team])
	teamorig_guid += (c.fetchall())
	c.execute('SELECT * FROM t_teams WHERE GUID = ?',teamorig_guid[team])
	original_teams += (c.fetchall()[0],)

#Make sure all teams are custom - the original team versions are not built-in
custom_season = False
custom_team = 0
for team in range(0,len(original_teams)):
	if(original_teams[team][1] is None and original_teams[team][3]==0):
		custom_team+=1

if(custom_team==len(original_teams)):
	custom_season=True
	print("\nCustom season found, beginning update process.")
	print("\nShould new rookies be all female (1), all male (2), or both (3)")
	temp = input('1, 2, or 3?')
	while(temp.strip() != '1' and temp.strip() != '2' and temp.strip() !='3'):
		temp = input('\nNot a valid option. 1, 2, or 3?')
	gender_gen = int(temp.strip())
	
else:
	print("\nERROR: Not a custom season.  Press enter to close")
	input()
	teardown()

#Store player team id
c.execute('SELECT playerTeamGUID FROM t_seasons WHERE GUID = ?',(seasons_incomplete[season][0],))
player_team_id = c.fetchone()
				

				
updated_custom_pd = []
updated_org_pd = []

retired_custom_local_id = []
retired_org_local_id = []

retired_org_po = []
retired_custom_po = []

stats = ['Position','Power', 'Contact', 'Speed', 'Fielding', 'Arm', 'Velocity', 'Junk', 'Accuracy']
row_format = "{:<25}"+"{:<19}"+"{:<11}" * ((len(stats)-1))
positions = [' P',' C','1B','2B','3B','SS','LF','CF','RF']
pitches = ['4F','2F','SB','CH','FK','CB','SL','CF']
#update the player information for each team, one team at a time
automate = False
for team in range(0,len(players_to_write)):

	current_team=[];
	cplayers_local_ids = []
	oplayers_local_ids = []
	players_positions = []
	players_names = []
	for player in range(0,len(players_to_write[0])):
		c.execute('SELECT * FROM t_baseball_player_local_ids WHERE GUID = ?',(players_to_write[team][player][0],))
		cplayers_local_ids += c.fetchall()
		c.execute('SELECT * FROM t_baseball_player_local_ids WHERE GUID = ?',(players_to_write[team][player][1],))
		oplayers_local_ids += c.fetchall()
		c.execute('SELECT optionValue FROM t_baseball_player_options WHERE baseballPlayerLocalID = ? AND optionKey = 66',(cplayers_local_ids[player][0],))
		first_name = (c.fetchall()[0])
		c.execute('SELECT optionValue FROM t_baseball_player_options WHERE baseballPlayerLocalID = ? AND optionKey = 67',(cplayers_local_ids[player][0],))
		last_name = (c.fetchall()[0])
		players_names += (first_name+last_name,)
		c.execute('SELECT optionValue FROM t_baseball_player_options WHERE baseballPlayerLocalID = ? AND optionKey = 54',(cplayers_local_ids[player][0],))
		players_positions += (c.fetchall()[0])
		current_team += (players_to_write[team][player],)

	print("\n\n{:<20}".format(custom_teams[team][2]))
	print(row_format.format("",*stats))
	
	datatup = []
	retiring = []
	
	for player in range(0,len(current_team)):
		data = list(current_team[player][3:])
		datastr = (positions[players_positions[player]-1],)
		if(random() < (.25+((sum(data[0:5])+.6*sum(data[5:]))*100-300)/300)):
			retired = True
			retiring += [player,]
			retired_custom_local_id += (cplayers_local_ids[player],)
			retired_org_local_id += (oplayers_local_ids[player],)
		else:
			retired = False
		for i in range(0,len(data)):
			data[i] = round(data[i]*100)
			if(data[7] > 0 and i > 4):
				upgrade = randint(0,5)+randint(0,5)
			elif(data[7] > 0 and i < 5):
				upgrade = randint(0,2)+randint(0,2)
			elif(data[7]==0 and i < 5):
				upgrade = randint(0,5)+randint(0,5)
			else:
				upgrade = 0
			data[i] += upgrade
			if (data[i] > 99):
				data[i]=99
			if(retired):
				datastr += ("Retired",)
			else:
				datastr += (str(data[i]-upgrade)+"+"+str(upgrade)+"("+str(data[i])+")",)
		datatup += (current_team[player][0:3]+tuple([x / 100 for x in data]),)
		print(row_format.format(str(player+1)+" "+players_names[player][0]+" "+players_names[player][1],*datastr))
	if(not automate):
		input("\nTeam progression complete for "+custom_teams[team][2]+".  Replacing retired players, press enter to continue.")
	
	replacing = [];
	new_players = [];
	for player in retiring:
		position = positions[players_positions[player]-1]
		replacing += [position]
		
		#create new players
		pitch_type_str = []
		if(position==' P'):
			c.execute('SELECT optionValue FROM t_baseball_player_options WHERE baseballPlayerLocalID = ? AND optionKey = 57',(cplayers_local_ids[player][0],))
			pitcher_role = c.fetchone()[0]
			if(pitcher_role ==1):
				position = 'SP:'
			elif(pitcher_role ==2):
				position = 'RP:'
			else:
				position = 'CP:'
			new_player = [create_pitcher(),create_pitcher(),create_pitcher()]
			pitch_types = [random_pitches(position[0:2]),random_pitches(position[0:2]),random_pitches(position[0:2])]
			for i in range(0,len(pitch_types)):
				temp = ''
				for j in range(0,len(pitch_types[i])):
					temp += (pitches[pitch_types[i][j]-1])
					if (j < len(pitch_types[i])-1):
						temp += ','
				pitch_type_str += (temp,)
		else:
			new_player = [create_player(),create_player(),create_player()]
			pitch_type_str = ['','','']
		
		new_pnames = []
		new_pgender = []
		for i in range(0,len(new_player)):
			if(gender_gen == 3):
				gender = randint(1,2)
			else:
				gender = gender_gen
			if (gender==1):
				firstname = choice(female_names)
			else:
				firstname = choice(male_names)
			lastname = choice(last_names)
			new_pnames += ((firstname,lastname),)
			new_pgender += (gender,)
				
		print("\n")
		print(row_format.format("",*stats))
		
		for i in range(0,len(new_player)):
			print(row_format.format(str(i+1)+'. '+new_pnames[i][0]+' '+new_pnames[i][1],position+pitch_type_str[i],*new_player[i]))
		
		manual = players_to_write[team][0][2]==player_team_id[0]
		if(not automate or manual):
			decision = input('Choose a player for '+position[0:2]+', or enter 4 to automate (Player team will not be automated):')
			while(not(decision.strip()=='1' or decision.strip()=='2' or decision.strip()=='3' or (decision.strip()=='4' and not manual))):
				decision = input('Not a valid option.  Try Again:')
			decision = int(decision.strip())
			if(decision==4):
				automate = True
		if(automate and not manual):
			total = 0
			index = 0
			for k in range(0,len(new_player)):
				value = sum(new_player[k])
				if (value > total):
					total = value
					index = k
			decision = index+1
		
		
		datatup[player] = current_team[player][0:3]+tuple(x/100 for x in new_player[decision-1])
		players_names[player] = new_pnames[decision-1]
		
		#update player options for the local ID
		retired_custom_po += ((cplayers_local_ids[player][0], 66, players_names[player][0], 4),)
		retired_custom_po += ((cplayers_local_ids[player][0], 67, players_names[player][1], 4),)
		
		#handle pitcher options
		if(position[0:2]=='SP' or position[0:2]=='RP' or position[0:2]=='CP'):
			retired_custom_po += ((cplayers_local_ids[player][0], 57, pitcher_role, 5),)
			for i in range(0,len(pitches)):
				try:
					pitch_types[decision-1].index(i+1)
					retired_custom_po += ((cplayers_local_ids[player][0], 58+i, 1, 5),)
				except:
					retired_custom_po += ((cplayers_local_ids[player][0], 58+i, 0, 5),)
			retired_custom_po += ((cplayers_local_ids[player][0], 48, randint(0,4), 5),)
			retired_custom_po += ((cplayers_local_ids[player][0], 49, randint(0,3), 5),)
		else:
			retired_custom_po += ((cplayers_local_ids[player][0], 48, 4, 5),)
			retired_custom_po += ((cplayers_local_ids[player][0], 49, 3, 5),)
		
		#handle gender specific options
		temp = gen_gender_po(cplayers_local_ids[player][0],new_pgender[decision-1])
		retired_custom_po += temp
		
		#gen all other options
		temp = gen_generic_po(cplayers_local_ids[player][0])
		retired_custom_po += temp
		
	print("\nReplaced "+str(len(retiring))+" players with positions "+(str(replacing).replace('\'','')).strip('[]'))

	#Print out finalized team data
	print("\n\n{:<20}".format(custom_teams[team][2])+" updated roster:")
	print(row_format.format("",*stats))
	for j in range(0,len(current_team)):
		data = list(datatup[j][3:])
		datastr = (positions[players_positions[j]-1],)
		for i in range(0,len(data)):
			data[i] = round(data[i]*100)
			datastr += (str(data[i]),)
		print(row_format.format(str(j+1)+" "+players_names[j][0]+" "+players_names[j][1],*datastr))
	
	updated_custom_pd += datatup

#Copy the data custom season players to the original players (both are updated)
for i in range(0,len(updated_custom_pd)):
	c.execute('SELECT * FROM t_baseball_players WHERE GUID = ?', (updated_custom_pd[i][1],))
	temp = c.fetchone()
	updated_org_pd += (temp[0:3]+updated_custom_pd[i][3:],)

retired_org_po = []
for i in range(0,len(retired_custom_local_id)):
	for j in range(0,len(retired_custom_po)):
		if(retired_custom_local_id[i][0]==retired_custom_po[j][0]):
			retired_org_po += ((retired_org_local_id[i][0],)+retired_custom_po[j][1:],)
		
#update the sqlite database

#Delete old players from database
for team in range(0,len(teams)):
	c.execute('DELETE FROM t_baseball_players WHERE teamGUID = ?',teams[team])
	c.execute('DELETE FROM t_baseball_players WHERE teamGUID = ?',teamorig_guid[team])

#Add the new players to the database
c.executemany('INSERT INTO t_baseball_players VALUES (?,?,?,?,?,?,?,?,?,?,?)',updated_org_pd)
c.executemany('INSERT INTO t_baseball_players VALUES (?,?,?,?,?,?,?,?,?,?,?)',updated_custom_pd)

#Update the player options for the retired players (eventually randomize more of the options)
#for player in range(0,len(retired_custom_local_id)):
	#c.execute('DELETE FROM t_baseball_player_options WHERE baseballPlayerLocalID = ? AND optionKey != 53 AND optionKey != 54 AND optionKey != 55',(retired_custom_local_id[player][0],))
	#c.execute('DELETE FROM t_baseball_player_options WHERE baseballPlayerLocalID = ? AND optionKey != 53 AND optionKey != 54 AND optionKey != 55',(retired_org_local_id[player][0],))

c.executemany('REPLACE INTO t_baseball_player_options VALUES (?,?,?,?)',retired_custom_po)
c.executemany('REPLACE INTO t_baseball_player_options VALUES (?,?,?,?)',retired_org_po)
	
conn.commit()
conn.close()

#Repack into the new save file
with open('database.sqlite', 'rb') as new_data:
    new_save = new_data.read()
zlib_save = zlib.compress(new_save)
f = open('savedata_new.sav', 'wb')
f.write(zlib_save)
f.close()

os.remove('database.sqlite')
input('\nProcess Completed!  Updated file saved as \'savedata_new.sav\'.  Press enter to close.')
