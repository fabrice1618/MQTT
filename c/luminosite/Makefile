subscribe: subscribe.c
	gcc subscribe.c -o subscribe -lmosquitto

luminosite: luminosite.c cJSON.h cJSON.c
	gcc luminosite.c cJSON.c -o luminosite -lmosquitto

read_data: read_data.c cJSON.h cJSON.c
	gcc read_data.c cJSON.c -o read_data -lmosquitto
