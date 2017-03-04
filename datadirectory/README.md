## Dataserver directory structure:
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
 (dockserver mirror part:)
--/logs
--- glider log files from the dockserver
--/from-glider
--- data files retrieved from the glider
--/to-glider
--- files to send to the glider

```
