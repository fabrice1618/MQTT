v1: v1.c ../cJSON.h ../cJSON.c
	gcc v1.c ../cJSON.c -o v1 -lmosquitto

v2: v2.cpp ../cJSON.h ../cJSON.c Luminosite.h Luminosite.cpp
	g++ v2.cpp ../cJSON.c Luminosite.cpp -o v2 -lmosquitto

clean:
	rm v1
	rm v2