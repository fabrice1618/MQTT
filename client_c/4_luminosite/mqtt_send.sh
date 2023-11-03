#!/bin/bash
while true
do
    mosquitto_pub -h 127.0.0.1 -t "sensor/luminosite" -m '{"capteur":"capteur1", "mesures":[480,480,481,481,481,480,480,480]}'
    sleep 2
done