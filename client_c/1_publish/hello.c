#include <stdio.h>
#include <string.h>
#include <mosquitto.h>

#include "../config.h"

int main(int argc, char *argv[]) 
{
    char *broker = BROKER;
    int port = BROKER_PORT;
    char *message = "hello world !";
    char *topic = "hello";
    struct mosquitto *client;
    int ret = 0;
    
    mosquitto_lib_init();   // initialise la bibliothèque
    
    // crée un client    
    // parametres : generate an id, create a clean session, no callback param 
    client = mosquitto_new(NULL, true, NULL);
    
    ret = mosquitto_connect(client, broker, port, false); // pas de connexion persistante
    if (ret != MOSQ_ERR_SUCCESS) {
        perror("mosquitto_connect");
        return(ret);        
    }
    
    // publie un message dans le sujet
    // parametres : client handle, message id, topic, length of message, message to be sent, QoS, retained
    mosquitto_publish(client, NULL, topic, strlen(message)+1, (const void *)message, 0, false);

    mosquitto_destroy(client);  // détruit le client
    mosquitto_lib_cleanup();    // libère les ressources MQTT
    
    return 0;
}