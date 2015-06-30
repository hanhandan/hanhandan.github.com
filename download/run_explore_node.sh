#!/bin/sh
while [ `date +%Y` -lt 2015 ]; do
    sleep 1
done

while :
do
    stillRunning=`ps |grep "explore_node" |grep -v "grep" | grep -v "run_explore_node.sh"`
    if [ "$stillRunning" ] ; then
        exit 1
    else                                
        /thunder/bin/readkey sn | grep "data:" | awk -F " " '{print $NF}' | xargs /thunder/bin/miner_32/explore_node &
        exit 0
    fi
done
