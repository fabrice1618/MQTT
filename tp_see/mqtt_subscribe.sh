#!/bin/bash

mosquitto_sub -h localhost --username "hello" --pw "hello_world" -t "sensors/bureau/temperature" -t "sensors/bureau/normalise" -t "sensors/bureau/controle"
