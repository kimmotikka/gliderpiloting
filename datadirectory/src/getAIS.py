# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
# 
#	1) active missions in <rootdir>/forweb/current_missions.txt
#   2) get logfiles from active missions
#	3) parse active json files 
#	4) create AIS-requests 
#	5) request AIS-data, if requests exists
#	6) remove AIS-request file (aisQ.sh)
#	7) collect json data 
#	8) transfer to webserver
#
#	rootdir: /data/gliders/
#							/simulate/s_tvar
#					  	   	/uivelo
#	
#	<rootdir>/forweb/current_missions.txt 
#   example: s_tvar tvar2017 simulate/s_tvar
#
#	list of read logfiles gliderdataroot/data/glider-readFiles.txt
#	processed gliderdata into gliderdataroot/data
#
#   <rootdir>/forweb/aisQ.sh
#	
import datetime 
import os
import json

TDELTA = 5 # age of the AIS data requested [hours before current] 
RADIUS = 200 # max distance from glider position [km]


def readJson(fdir, jfile):
  ''' read json-file: '''
  try:
      f = open(fdir + '/' + jfile, "r")
  except IOError, e:
      raise IOError
  else:
      data = json.loads(f.read())
      f.close()
  return(data)

def getFileNames(directory, glider, wildchar, logs=False, readFileName=""):
	'''Read filenames and drop allready read files
		directory: gliders dockservermirror-root...
	'''
	if (logs):
		dataFiles = os.listdir(directory+'/logs/')
	else:
		dataFiles = os.listdir(directory)
	dataFiles = [s for s in dataFiles if (wildchar in s)]
	if (logs):
		'''luetaan log-tiedostoja'''
		dataFiles = [s for s in dataFiles if (glider in s)]
		if (readFileName == "") :
			rf = directory+'/data/'+glider+'-filesRead.txt'
		readFiles = []
		try: 
			if os.path.isfile(rf):
				with open(rf, 'r') as readF:
					for r in readF:
						readFiles.append(r[:-1])
			if (readFiles != []):
				dataFiles = [s for s in dataFiles if s not in readFiles]
		except SyntaxError:
			print "error: ", rf

	return dataFiles


# data per glider:
def getActiveMissions(rootdir):
	'''read current-missions.txt from <dataroot>/forweb directory'''
	missions = []
	try: 
		with open(rootdir+'/forweb/current_missions.txt', "r") as cm:
			for line in cm:
				if not ('#' in line[0:5]):
					#print line
					d = line[:-1].split(' ') #mission.append(line[:-1].split(' '))
					#print d
					missions.append({"glider": d[0], "mission":d[1], "rootdir":d[2], "startDate":d[3], "startTime":d[4]})	
	except Exception:
		pass
	return missions

def getLastPositions(root, missions):
	positions = []
	for m in missions:
		try: 
			missData = readJson(root+'/'+m["rootdir"]+'/data/', m["glider"]+'_'+m["mission"]+'.json')
		except IOError:
			pass
		else:
			try:
				lastpos = {"glider": missData["glider"], "mission":missData["mission"], "lastTime":missData["lastTime"], "lastPosition":missData["path"][-1]}
				positions.append(lastpos)
			except IndexError:
				pass
	return positions

def getGliderPath(root, missions):
	path = []
	for m in missions:
		try: 
			missData = readJson(root+'/'+m["rootdir"]+'/data', m["glider"]+'_'+m["mission"]+'.json')
		except IOError:
			pass
		else:
			gliderPath = {"glider": missData["glider"], "lastTime":missData["lastTime"], "path":missData["path"]}
			path.append(gliderPath)
	return path

def getMissionPosition(mission, positions):
	pos = []
	for p in positions:
		if (mission["glider"]==p["glider"]) and (mission["mission"]==p["mission"]):
			pos = p["lastPosition"]
			break
	return pos

def setAISCommand(rootdir):
	'''create AIS-data requests'''

	missions = getActiveMissions(rootdir)
	positions = getLastPositions(rootdir, missions)
	aisDataDir = rootdir+'/forweb/'
	aisSH = aisDataDir + 'aisQ.sh'

	#currentTime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
	cTime = datetime.datetime.now()  + datetime.timedelta(hours=-TDELTA) 
	AISTime = cTime.isoformat('T')+'Z' #strftime("%Y-%m-%D %Z")
	for m in missions:
		print m["glider"], m["mission"]
		if (getMissionPosition(m, positions) != []): 
			xlast = getMissionPosition(m, positions)
			aisDataDir = rootdir+'/'+m["rootdir"]+'/data' #'/Users/tikkak/nodc/dev/uivelo/simulate/testi/'
			aisFile = aisDataDir + '/'+m["glider"]+'_'+m["mission"]+'_ais.json'

			aisURL = "'http://meri-test.digitraffic.fi/api/v1/locations/latitude/"+str(xlast[0])+"/longitude/"+str(xlast[1])+"/radius/"+str(RADIUS)+"/from/"+AISTime+"'"
			curl = "curl -s -X GET --header 'Accept: application/json' "+aisURL + " > " + aisFile
			# set also http-proxy:
			#curl = "curl -s  --proxy <http-proxy> -X GET --header 'Accept: application/json' "+aisURL + " > " + aisFile
			#aistmp.txt"

			print curl

			if os.path.isfile(aisSH):
				with open(aisSH, "a") as sf:
				 	sf.write(curl+'\n')
			else:
				with open(aisSH, "w") as sf:
				 	sf.write(curl+'\n')

def combineJSON(root):
	missions = getActiveMissions(root)
	aisdata = []
	plans = []
	paths = []

	aisStr = 'var shipCollection = '
	planStr = 'var plans = '
	pathStr = 'var paths = '

	for m in missions:
		mDataDir = root+'/'+m["rootdir"]+'/data/'
		try: 
			with open(mDataDir+m["glider"]+'_'+m["mission"]+'_ais.json',"r") as jsonais:
				ais = json.load(jsonais)
			aisdata.append(ais)
		except (IOError, ValueError):
			pass
		try: 
			with open(mDataDir+m["glider"]+'_'+m["mission"]+'_plan.json',"r") as jsonplan:
				plan = json.load(jsonplan)
			plans.append(plan)
		except (IOError, ValueError):
			pass
		try:
			with open(mDataDir+m["glider"]+'_'+m["mission"]+'.json',"r") as jsonpath:
				path = json.load(jsonpath)
			paths.append(path)
		except (IOError, ValueError):
			pass
	
	try:
		with open(root+'/forweb/current-ais.js',"w") as ais:
			ais.write(aisStr)
			ais.write(json.dumps(aisdata))
			ais.write(';')
	except (IOError, ValueError):
		pass
	try:
		with open(root+'/forweb/current-plans.js',"w") as planf:
			planf.write(planStr)
			planf.write(json.dumps(plans))
			planf.write(';')
	except (IOError, ValueError):
		pass
	try:
		with open(root+'/forweb/current-paths.js',"w") as pathf:
			pathf.write(pathStr)
			pathf.write(json.dumps(paths))
			pathf.write(';')
	except (IOError, ValueError):
		pass

	with open(root+'/forweb/current-positions.js',"w") as posf:
		
		posf.write(json.dumps(getLastPositions(root, missions)))


if __name__ == '__main__':
	'''Haetaan AIS-data'''
	# directory = 'test'
	# glider = 'uivelo'
	# mission = 'syksy'
	print "Hello world!"
	#getAIS('uivelo-tvar2017')

