#!/bin/sh
# put this script in crontab
# e.g. 
# */10 * * * * sh getAIS.sh
#
rootdir=/data/gliders
sourcedir=$rootdir/src
webdir=$rootdir/forweb
cd $sourcedir
<pythonpath>/python -c "import read_gliderlog as rg; rg.writeCurrentMissionData('$rootdir');"
#
echo "delete old sh:n"
rm -f $webdir/aisQ.sh
# form AIS-data requests:
echo "write ais-requests"
<python path>/python -c "import getAIS; getAIS.setAISCommand('$rootdir')"
# request AIS data:
echo "AIS-requests"
sh $webdir/aisQ.sh
echo "Ok!"
#
# combine json files:
#
<python path>/python -c "import getAIS; getAIS.combineJSON('$rootdir')"
#
# direct and freewave on-bench simulation appends logs into one file, real missions create a new file for every surfacing
# this needs some modification in the python code
# with move (could be also rm) commands logfiles are read every time  
#LATEST=`date +"%Y%m%d_%H%M%S"`
#mv $rootdir/simulate/sim_uivelo/data/sim_uivelo-filesRead.txt $rootdir/simulate/sim_uivelo/data/sim_uivelo-filesRead.txt.$LATEST
#mv $rootdir/simulate/s_aland/data/s_aland-filesRead.txt $rootdir/simulate/s_aland/data/s_aland-filesRead.txt.$LATEST
