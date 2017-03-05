# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
# 
# Kimmo Tikka / Finnish Meteorological Institute
# c kimmo.tikka@fmi.fi

'''
<start:b_arg>				
b_arg: start_when(enum) 0				
b_arg: list_stop_when(enum) 007				
b_arg: initial_wpt(enum)  -1  # one after last one achieved				
b_arg: num_legs_to_run(nodim)   -2    #  traverse list once (stop at last in list)				
b_arg: num_waypoints(nodim) 11			
<end:b_arg>				
<start:waypoints>				
#WPT FORMAT: (DDmm.mmm)				
# longitude	latitude	koodi	nimi	
#1944.0975	6003.5516	#   0	G1_1	
1932.7129	5957.1555	#   1	G1_2	
1929.5823	5958.9888	#   2	G2_2	
1940.1711	6004.9081	#   3	G2_1	
'''
#import simplekml
import json

def readMaFile(maf):
	ma = {"b_arg":[], "coords":[]}
	with open(maf, 'r') as maf:
		barg = 0
		wpt = 0
		cc = []
		for l in maf:
			if "behavior" in l:
				ma["behavior"] = l.split("\t")[0]
			elif "#" in l[0:1]:
				cc.append(l)
			elif "start:b_arg" in l :
				barg = 1
			elif "end:b_arg" in l :
				barg = 0
			elif "start:waypoints" in l :
				wpt = 1
			elif "end:waypoints" in l :
				wpt = 0
			elif barg == 1:
#				print "barg: " + l
				la = l.split(':')
				la1 = la[1].split('(')
				la2 = la1[1].split(')')
				if "#" in la2[1]:
					lac = la2[1].split("#")[1]
					lav = int(la2[1].split("#")[0].strip())
				else:
					lac = ""					
					lav = int(la2[1].strip())
				arg = {la1[0].strip():lav,"type":la2[0],"comment":lac.strip()}
				ma["b_arg"].append(arg)
			elif wpt == 1:
				#print "wpt: " + l
				lcom = l.split('#')[1]
				lc = l.split('#')[0].split()
#				1940.1711	6004.9081	#   3	G2_1
				name = str(lcom).split()[1]	
				#print lc
				lond = lc[0][0:2] 
				lonm = lc[0][2:]
				latd = lc[1][0:2]
				latm = lc[1][2:]
				dlon = float(lond) + (float(lonm)/60)
				dlat = float(latd) + (float(latm)/60)
				dlon = float("{0:.4f}".format(dlon))
				dlat = float("{0:.4f}".format(dlat))

#				print lc[0], lond, lonm, lc[1], latd, latm
				coord = {"glon":lc[0], "glat":lc[1], "dlon":dlon, "dlat":dlat, "comment":lcom.strip(), "name":name}
				ma["coords"].append(coord)
			else:
				pass
			ma["comments"] = cc
	return ma

# def writeKML(glider, mission, plan, kmlout):
# 	#Writing the kml file.
# 	f = open(kmlout, "w")
# 	f.write("<?xml version='1.0' encoding='UTF-8'?>\n")
# 	f.write("<kml xmlns='http://earth.google.com/kml/2.1'>\n")
# 	f.write("<Document>\n")
# 	f.write("   <name>" + kmlout + '.kml' +"</name>\n")
# 	for m in plan:
# 		for c in m["coords"]:
# 		    f.write("   <Placemark>\n")
# 		    f.write("       <name>" + str(c["name"]) + "</name>\n")
# 		    f.write("       <description>" + c["glon"]+ ' ' + c["glat"] + "</description>\n")
# 		    f.write("       <Point>\n")
# 		    f.write("           <coordinates>" + str(c["dlon"]) + "," + str(c["dlat"]) + "," + str(0) + "</coordinates>\n")
# 		    f.write("       </Point>\n")
# 		    f.write("   </Placemark>\n")
# 	f.write("</Document>\n")
# 	f.write("</kml>\n")
# 	f.close()
# 	return 1

def writeGMTxy(glider, mission, plan, fileout):
	fo = open(fileout, "w")
	for g in plan:
		fo.write('>\n')
		for c in g["coords"]:
			fo.write(str(c["dlon"])+'\t'+str(c["dlat"])+'\n')
	fo.close()
	return 1

def writeJS(glider, mission, plan):
	planjs = {"glider": glider, "mission":mission, "plan":[]}
	for g in plan:
		for c in g["coords"]:
			planjs["plan"].append([c["dlat"], c["dlon"]])
	return planjs

if __name__ == '__main__':
	'''Parsing missions goto ma-files'''
	# numbers xx of the goto_lxx.ma files to parse
	mafiles = [38,39]
	gpath = '-'.join(str(i) for i in mafiles)
	madir = '/data/gliders/tmp/'
	mission = []
	for m in mafiles:
		mafile = madir + 'goto_l'+str(m)+'.ma'
		mission.append(readMaFile(mafile))

	writeGMTxy(mission, './test-'+gpath+'.xy')
	writeKML(mission, './test-'+gpath+'.kml')
	writeJS(mission, './test-'+gpath+'.js')
