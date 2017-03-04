# gliderpiloting
Software to manage glider missions on web 

This project is for manage glider missions and simulations

1) Position of the glider with AIS data layer on web
- python code to parse the glider position from log files
- command to request AIS data from Finnish Transport Agency's service (in the Baltic Sea area)
- web page with some javascript to show the data

For retrieving the glider log from the dockserver I used John Kerfoot's dockserver mirroring system:
https://github.com/kerfoot/dockserver-mirror

###Dataserver directory structure:
```
<gliderfiles root>
-/src
--- source codes
-/forweb
-- active mission configuration: current_missions.txt
-- jsonfiles generated
-/<glider directories>
--/data: data for the 
--- goto_lxx.ma files of the mission
--- generated files
dockserver mirror:
--/logs
--- glider log files from the dockserver
--/from-glider
--- data files retrieved from the glider
--/to-glider
--- files to send to the glider
```
###Webserver
```
<web path>
- webpage for the map and data
-/js
-- javascript codes
-/icons
-- icons and pictures
-/current
-- json files with gliderdata
--- current-path.json
--- current-path.json
--- current-AIS.json
```
