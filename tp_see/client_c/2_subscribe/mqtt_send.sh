#!/bin/bash
while true
do
    mosquitto_pub -h localhost --username "hello" --pw "hello_world" -t "sensors/bureau/temperature" -m "{'timestamp':123456, 'temperature':12.3}"
    sleep 2
done