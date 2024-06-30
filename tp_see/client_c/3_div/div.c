#include <stdio.h>
#include <string.h>

#define SENSOR_DATA "{'timestamp':123456, 'temperature':12.3}"

void construction()
{
    char *format = "message = {'user_name': '%s','minute': %d, 'temperature': %4.1f}";
    char message[200];
    char *user = "user test";
    int minute = 42;
    float temperature = 12.3;

    sprintf(message, format, user, minute, temperature);
    printf("construction JSON: %s\n", message);
}

void analyse()
{
    char *sensor_data = SENSOR_DATA;
    int timestamp;
    float temperature;

    printf("Analyse de: %s\n", sensor_data);
    sscanf( sensor_data, "{'timestamp':%d, 'temperature':%f}", &timestamp, &temperature );
    printf("Valeurs: %d %f\n", timestamp, temperature);
}

int main(int argc, char *argv[]) 
{
    analyse();
    construction();
}
