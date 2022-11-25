 
#!bin/bash

docker ps -a --format "{{.Names}}" > /opt/cecil/TEMP/container_names

# python3 monitor.py --container-name hbbr
File='/opt/cecil/TEMP/container_names'
names=$(cat $File)
for Line in $names
do
        echo "Testing $Line for issues"
        python3 /opt/cecil/monitor-docker/monitor.py $1 --container-name "$Line"
done

rm /opt/cecil/TEMP/container_names