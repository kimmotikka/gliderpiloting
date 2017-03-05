# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
# Parsing Slocum gliders logfile
# Kimmo Tikka / Finnish MEteorological Institute
# kimmo.tikka@fmi.fi
#
import datetime
from datetime import datetime
import time
import json
import numpy as np
import os
import re

import getAIS as getAIS
import gotoFileParser as gotoFileParser

#dataDir = '/Users/tikkak/nodc/data/glider_Rutgers/dbdreader-0.3.7/logs/'

PSTRINGS = ['Curr Time', 'GPS Location','m_coulomb_amphr_total','m_battery','m_lat','m_lon', 'c_wpt_lat', 'c_wpt_lon', 'm_leakdetect_voltage(', 'm_leakdetect_voltage_forward', 'Waypoint']

# rf = './tmp/readLogfiles.csv'
# valueFile = './tmp/values.tsv'
# voltageMeanFile = './tmp/voltage.tsv'
# locatFile = './tmp/locat.csv'
# courseFile = './tmp/course.js'
# voltageStart = './voltage_start.csv'

def column(matrix, i):
    return [row[i] for row in matrix]

def createDateObject(presentTime): 
	'''Nykyhetkesta aikaobjekti'''
	return datetime.fromtimestamp(presentTime)

def FormatDate(objectDate,strFormat="%Y-%m-%d %H:%M:%S"):
	'''Ajan tulostus maaraformaatissa YYYY-MM-DD HH:MM:SS'''
	return objectDate.strftime(strFormat)

def formatPresentTime(presentTime,strFormat="%Y-%m-%d %H:%M:%S"):
	'''Nykyhetken tulostus maaraformaatissa YYYY-MM-DD HH:MM:SS'''
	return datetime.fromtimestamp(presentTime).strftime(strFormat)

def dateform(tstr):
	t = tstr.split(' ')
	ts = t[5]+'-11-'+t[3]+' '+t[4][0:3]
	#print t, ts
	return ts

def dmm2dd(ddmmm):
	'''ddmm.mmm koordinaatit desimaaleiksi'''
	try: 
		d = float(ddmmm[0:2])+float(ddmmm[2:])/60.0
	except ValueError:
		print "dd: ", ddmmm
	try:
		ddddd = float("{0:.4f}".format(d))
	except (ValueError, UnboundLocalError):
		print "dmuun: ", ddmmm
		return -1.0
	else:
		return ddddd


def readJson(fdir, jfile):
  ''' Luetaan json-tiedosto: '''
  try:
      f = open(fdir + '/' + jfile, "r")
  except IOError, e:
      raise IOError
  else:
      data = json.loads(f.read())
      f.close()
  return(data)

def parseString(stri, var):
	'''Puretaan logitiedoston datarivin arvot'''
	str1 = re.sub(' +', ' ', stri)[:-1]
	if (var == 'Curr Time'):
		try: 
			return FormatDate(datetime.strptime(str1.split('Time:')[1].split('MT')[0].strip(), '%a %b %d %H:%M:%S %Y'))
		except IndexError:
			return -1
	elif (var == 'GPS Location'):
#		GPS Location:  5945.987 N  2122.567 E measured       2.04 secs ago
		lat = str1.split(':')[1].split(' ')[1]
		lon = str1.split(':')[1].split(' ')[3]
		#print lat + ';' + lon
		return lat+';'+lon
	elif (var == 'Waypoint:'):
		return str1.split("point:")[1]
	else:
		try: 
			return "%.5f" % float(str1.split('=')[1].split(' ')[0])
		except IndexError:
			# print " ####2 ", var
			# print str1
			return -1

def parseLogData(bdir, gfile):
	'''parse data from logfile'''
	lati = PSTRINGS.index("m_lat")
	loni = PSTRINGS.index("m_lon")
	coordi = PSTRINGS.index("GPS Location")

	lc = []
	volt = []
	timestr = ''
	locat_lat = 0
	locat_lon = 0
	battery = ''
	valuex = ['']*len(PSTRINGS)
	values = []
	if os.path.isfile(bdir+'/'+gfile):
		print "tiedosto on : ",bdir+'/'+gfile
	else:
		print "tiedostoa ei ole: ", bdir+'/'+gfile
	try: 
		with open(bdir+'/'+gfile, 'r') as logis:
			#print bdir+gfile
			nr = 0
			for str0 in logis:
				nr += 1
	#			print "SSS ", str0[:-1]
				str0 = str0[:-1]
				sind = -1
				var = 0
				try:
					if (str0.index('Curr Time') > -1) and (valuex[PSTRINGS.index('Curr Time')]):
						#print nr, valuex
						if (str(valuex[loni]) != '') and (str(valuex[loni]) != '-1') and (str(valuex[loni]) != '-1.0'):
							try:
								valuex[lati] = dmm2dd(valuex[lati])
								valuex[loni] = dmm2dd(valuex[loni])
							except ValueError:
								print "m_ ", valuex
						else:
							#print coordi, valuex[coordi], valuex[coordi][0], valuex[lati], valuex[loni] 
							try:
								crd = valuex[coordi].split(';')
								valuex[lati] = dmm2dd(crd[0])
								valuex[loni] = dmm2dd(crd[1])
							except ValueError:
								print "gps: ",valuex
						values.append(valuex)
						valuex = ['']*len(PSTRINGS)
				except ValueError:
					pass
				for s in PSTRINGS:
	#				print "pp ", s, str0
					try: 
						sind = str0.index(s)
					except ValueError:
						sind = -1
						pass
					else:
						if (sind > -1):
							var = s
							#print "sss ", var, s 
							break
				if (sind > -1):
					try: 
						valuex[PSTRINGS.index(var)] = str(parseString(str0, var)).strip()
					except Exception:
						pass
					sind = -1

			#print "r: ", valuex[coordi], valuex[lati], valuex[loni]
			if (str(valuex[lati]) != '') and (str(valuex[lati]) != '-1') and (str(valuex[lati]) != '-1.0'):
				try:
					valuex[lati] = dmm2dd(valuex[lati])
					valuex[loni] = dmm2dd(valuex[loni])
				except ValueError:
					print "m_ ", valuex
			else:
				try:
					valuex[lati] = dmm2dd(valuex[coordi].split(';')[0])
					valuex[loni] = dmm2dd(valuex[coordi].split(';')[1])
					#print valuex[coordi], valuex[lati], valuex[loni]
				except (ValueError, IndexError):
					print "gps: ",valuex
			values.append(valuex)
	except SyntaxError:
		print bdir+'/'+gfile
	return values

def values2JSON(glider, mission, valuearr, headers):
	'''logs to json'''
	lati = headers.index("m_lat")
	loni = headers.index("m_lon")
	coordi = headers.index("GPS Location")
	timi = headers.index("Curr Time")
	#print column(valuearr, valuearr[timi])
	start =  min(column(valuearr, timi))
	last = max(column(valuearr, timi))
	#print lati, loni, timi
	jsonvalues = {"glider":glider, "mission": mission, "path":[], "startTime": start, "lastTime":last, "data":[]}
	#print json.dumps(jsonvalues)
	for d in valuearr:
		#print d[0][timi]
		lat = d[lati]
		lon = d[loni]
		if (str(lon) != '-1') and (str(lon) != '') :
			jsonvalues["path"].append([lat,lon])
		datarow = {}
		for i in range(len(headers)-1):
			datarow[headers[i]] = d[i]
		jsonvalues["data"].append(datarow)
	return jsonvalues

 # "data": [
  #   {
  #     "m_lon": "1948.73760",
  #     "m_coulomb_amphr_total": "32.95000",
  #     "m_leakdetect_voltage(": "2.48065",
  #     "c_wpt_lon": "1948.74510",
  #     "m_battery": "14.12803",
  #     "m_leakdetect_voltage_forward": "2.47570",
  #     "GPS Location": "60.0623/19.8123",
  #     "m_lat": "6003.73580",
  #     "Curr Time": "2016-11-10 11:58:49",
  #     "c_wpt_lat": "6003.66570"
  #   },
 
def getVoltageAve(jsonvalues):
	'''Lasketaan tuntikeskiarvot'''
	from itertools import groupby
	from operator import itemgetter

	volta = []
	for jv in jsonvalues["data"]:
		if (jv["m_battery"] != '-1'):
			datet = jv["Curr Time"][:13]
			voltage = float(jv["m_battery"])
			volta.append([datet, voltage])

	voltm = []
	for groupByID, rows in groupby(volta, key=itemgetter(0)):
	    counter, position1 = 0, 0
	    for row in rows:
	        position1+=row[1]
	        counter+=1
	    voltm.append([groupByID+':00:00', float("%.3f" % float(position1/counter))])

	voltage = {"glider":jsonvalues["glider"], "mission":jsonvalues["mission"], "volts":voltm}
	return voltage

def readLogFiles(root, m):
#
	headers = PSTRINGS
	lati = headers.index("m_lat")
	loni = headers.index("m_lon")
	coordi = headers.index("GPS Location")
#
	alldata = []
	logDir = root+'/'+m["rootdir"]+'/logs/'
	dataFiles = getAIS.getFileNames(root+'/'+m["rootdir"], m["glider"], 'log', logs=True)
	#dataFiles = os.listdir(logDir)
	#dataFiles = [s for s in dataFiles if glider in s ]
	dataFiles.sort()
	# print root, m["glider"], m["mission"], m["startDate"], m["startTime"], m["rootdir"], len(dataFiles)
	# for f in dataFiles:
	# 	print f
	if (dataFiles == []):
		return []
	#readFiles = []
	rfile = root +'/'+m["rootdir"]+'/data/'+m["glider"]+'-filesRead.txt'
	rf = open(rfile, 'a+')
	alldata = []
	for dataf in dataFiles:
		#print dataf
		values = parseLogData(logDir, dataf)
		if (values != []):
			alldata.extend(values)
			rf.write(dataf+'\n')
	alldata = [ v for v in alldata if (v[0] != '-1') and (v[0] != '')] #and (v[0] != '-1.0')]
	# otetaan mukaan vain data, joka on mission alun jalkeen kirjoitettu!
	alldata = [ v for v in alldata if (v[0] > m["startDate"]+' '+m["startTime"])]
	rf.close()
	print 'readLogFiles return: ', len(alldata) #, alldata[0][0]
	return alldata

	# for d in valuearr:
	# 	#print d[0][timi]
	# 	lat = dmm2dd(d[lati])
	# 	lon = dmm2dd(d[loni])
	# 	crd = d[coordi]
	# 	print lat, lon, crd
	# 	if (lon > 0.0) and (lon < 180.0) and (lat > 0.0):
	# 		jsonvalues["path"].append([lat,lon])
	# 	else:
	# 		jsonvalues["path"].append([crd["lat"], crd["lng"]])

def writeMissionJSON(root, m, alldata):
	'''kirjoitata aktiivisten missioiden data ja voltagen'''
	#missions = getAIS.getActiveMissions(root)
	jdata = values2JSON(m["glider"], m["mission"], alldata, PSTRINGS)
	gliderDataFile = root+'/'+m["rootdir"]+'/data/'+m["glider"]+'_'+m["mission"]+'.json'
	with open(gliderDataFile,"w") as gf:
		gf.write(json.dumps(jdata))

	gliderVoltageFile = root+'/'+m["rootdir"]+'/data/'+m["glider"]+'_'+m["mission"]+'_voltage.json'	
	volt = getVoltageAve(jdata)
	with open(gliderVoltageFile,"w") as gf:
		gf.write(json.dumps(volt))

def writeMissionData(root, m, alldata):
	gliderDataFile = root+'/'+m["rootdir"]+'/data/'+m["glider"]+'_'+m["mission"]+'.csv'
	if not (os.path.isfile(gliderDataFile)):
		with open(gliderDataFile,"w") as gf:
			header = '\t'.join([s for s in PSTRINGS])
			gf.write(header+'\n')
			for r in alldata:
				wstring = '\t'.join([str(s) for s in r])
				gf.write(wstring+'\n')
	else:
		with open(gliderDataFile,"a") as gf:
			for r in alldata:
				wstring = '\t'.join([str(s) for s in r])
				gf.write(wstring+'\n')

def writePlans(root):
	missions = getAIS.getActiveMissions(root)
	for m in missions:
		gotoFiles = getAIS.getFileNames(root+'/'+m["rootdir"]+'/data/', m["glider"], 'goto', logs=False)
		gotoFiles.sort()
		gotos = []
		for gf in gotoFiles:
			try:
				gotos.append(gotoFileParser.readMaFile(root+'/'+m["rootdir"]+'/data/'+gf))
			except Exception:
				pass
		if gotos != []:
			plan = gotoFileParser.writeJS(m["glider"], m["mission"], gotos)	
			with open(root+'/'+m["rootdir"]+'/data/'+m["glider"]+'_'+m["mission"]+'_plan.json', "w") as pf:
				pf.write(json.dumps(plan))

def writeCurrentMissionData(root):
	missions = getAIS.getActiveMissions(root)
	#print missions
	for m in missions:
		print 'readLogFiles: ', m
		data = readLogFiles(root, m)
		print 'data: ', len(data)
		if (data != []):
			writeMissionData(root, m, data)
			writeMissionJSON(root, m, data)
			#writeVoltageJSON(root, m, data)
	writePlans(root)

def main(glider, mission):
	'''Kaydaan lapi logitiedostoa ja etsitaan maaramuuttujat'''
	dataFiles = os.listdir(logDir)
	dataFiles = [s for s in dataFiles if glider in s ]
	dataFiles.sort()
	readFiles = []
	alldata = []
	for dataf in dataFiles:
		#print dataf
		values = parseLogData(logDir, dataf)
		alldata.extend(values)
	alldata = [ v for v in alldata if (v[0] != '-1') and (v[0] != '')]
	jdata = values2JSON('uivelo', 'aland2016', alldata, PSTRINGS)
	#print json.dumps(jdata)
	print json.dumps(getVoltageAve(jdata))

if __name__ == '__main__':
	# logDir = '/Users/tikkak/nodc/dev/uivelo/simulate/test/'
	# dataDir = '/Users/tikkak/nodc/dev/uivelo/simulate/test/data/'
	# main('uivelo', '201701')
	root = '/Users/tikkak/nodc/dev/uivelo/simulate/testi/data/'
	writeCurrentMissionData(root)
# rf = './tmp/readLogfiles.csv'
# valueFile = './tmp/values.tsv'
# voltageMeanFile = './tmp/voltage.tsv'
# locatFile = './tmp/locat.csv'
# courseFile = './tmp/course.js'
# voltageStart = './voltage_start.csv'
	
