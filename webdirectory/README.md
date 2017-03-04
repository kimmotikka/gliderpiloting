# Webpage to present glider position and AIS data

Ship icon color indicates the worst case (vessels direct distance to the glider / speed):
```
red: 0 - 1 h
orange: 1 - 2 h
yellow: 2 - 3 h
green: 3 - 4 h
blue: 4 - 5 h
gray: > 5 h
```

## Webserver
```
http://<web path>/current_mission.html
- webpage for the map and data
-/js
-- javascript codes
-/icons
-- icons and pictures
-/current
-- json files with gliderdata
--- current-path.json
--- current-path.json
--- current-AIS.json```
