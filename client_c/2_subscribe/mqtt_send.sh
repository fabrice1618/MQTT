#!/bin/bash
while true
do
    mosquitto_pub -h 127.0.0.1 -t "sensor/luminosite" -m '{"capteur":"capteur1", "mesures":[480,460,481,481,481,488,487,480]}'
    sleep 2
done