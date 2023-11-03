/*
 * This example shows how to write a client that subscribes to a topic and does
 * not do anything other than handle the messages that are received.
 */

#include <mosquitto.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "../config.h"
#include "../cJSON.h"

#define NOMBRE_MESURES 8
#define TOPIC_SEND "datastore/luminosite"
#define TOPIC_RECEIVE "sensor/luminosite"

typedef struct luminosite {
	char capteur[50];
	int lux;
} Luminosite;

// Variables globales
struct mosquitto *mosq;

void exit_error(const char *error_msg, int error_code) 
{
	if (error_msg != NULL) { 
		fprintf(stderr, "Code: %d, Error: %s\n", error_code, error_msg); 
		exit(error_code);
		} 
}

void remove_maxi(int *tab_mesure)
{
	int max_val = -1;
	int max_indice = 0;

	for(int i = 0; i < NOMBRE_MESURES; i++) {
		if (tab_mesure[i] > max_val) {
			max_val = tab_mesure[i];
			max_indice = i;
		}
	}
	tab_mesure[max_indice] = 0;
}

void remove_mini(int *tab_mesure)
{
	int min_val = 65536;
	int min_indice = 0;

	for(int i = 0; i < NOMBRE_MESURES; i++) {
		if (tab_mesure[i] < min_val && tab_mesure[i] > 0) {
			min_val = tab_mesure[i];
			min_indice = i;
		}
	}
	tab_mesure[min_indice] = 0;
}


int normalise(int *tab_mesure)
{
	int valeur = 0;
	int num_filtre = 0;
	int total = 0;

	for(int i = 0; i < NOMBRE_MESURES; i++) {
		if (tab_mesure[i] < 0) {
			tab_mesure[i] = 0;
			num_filtre++;
		}
		if (tab_mesure[i] > 65536) {
			tab_mesure[i] = 0;
			num_filtre++;
		}		
	}

	remove_maxi(tab_mesure);
	remove_mini(tab_mesure);
	remove_maxi(tab_mesure);
	remove_mini(tab_mesure);

	if (num_filtre < 4) {
		for(int i = 0; i < NOMBRE_MESURES; i++) {
			if (tab_mesure[i] > 0) {
				total += tab_mesure[i];
			}
		}
		valeur = total >> 2;
	}

	return valeur;
}


void analyse_payload(Luminosite *luminosite, char *msg_payload)
{
	strcpy(luminosite->capteur, "unknown");
	luminosite->lux = 0;

	// parse the JSON data 
	cJSON *json = cJSON_Parse(msg_payload); 
	if (json == NULL) { 
		const char *error_ptr = cJSON_GetErrorPtr();
		cJSON_Delete(json);
		exit_error(error_ptr, 1);
	} 

	// access the JSON data 
	cJSON *capteur = cJSON_GetObjectItemCaseSensitive(json, "capteur"); 
	if (cJSON_IsString(capteur) && (capteur->valuestring != NULL)) { 
		strcpy(luminosite->capteur, capteur->valuestring);
	} 

    const cJSON *mesure = NULL;
    const cJSON *mesures = NULL;
	int tab_mesure[NOMBRE_MESURES];
	int indice = 0;

	for(int i = 0; i < NOMBRE_MESURES; i++) {
		tab_mesure[i] = 0;
	}

    mesures = cJSON_GetObjectItemCaseSensitive(json, "mesures");
    cJSON_ArrayForEach(mesure, mesures)
    {
        if (cJSON_IsNumber(mesure) && (indice < NOMBRE_MESURES)) {
			tab_mesure[indice++] = (int)mesure->valuedouble;
        }
    }

	luminosite->lux = normalise(tab_mesure);

	// delete the JSON object 
	cJSON_Delete(json); 
}

/* Callback called when the client receives a CONNACK message from the broker. */
void on_connect(struct mosquitto *mosq, void *obj, int reason_code)
{
	int rc;
	/* Print out the connection result. mosquitto_connack_string() produces an
	 * appropriate string for MQTT v3.x clients, the equivalent for MQTT v5.0
	 * clients is mosquitto_reason_string().
	 */
	printf("on_connect: %s\n", mosquitto_connack_string(reason_code));
	if(reason_code != 0){
		/* If the connection fails for any reason, we don't want to keep on
		 * retrying in this example, so disconnect. Without this, the client
		 * will attempt to reconnect. */
		mosquitto_disconnect(mosq);
	}

	/* Making subscriptions in the on_connect() callback means that if the
	 * connection drops and is automatically resumed by the client, then the
	 * subscriptions will be recreated when the client reconnects. */
	rc = mosquitto_subscribe(mosq, NULL, TOPIC_RECEIVE, 1);
	if(rc != MOSQ_ERR_SUCCESS){
		fprintf(stderr, "Error subscribing: %s\n", mosquitto_strerror(rc));
		/* We might as well disconnect if we were unable to subscribe */
		mosquitto_disconnect(mosq);
	}
}


/* Callback called when the broker sends a SUBACK in response to a SUBSCRIBE. */
void on_subscribe(struct mosquitto *mosq, void *obj, int mid, int qos_count, const int *granted_qos)
{
	int i;
	bool have_subscription = false;

	/* In this example we only subscribe to a single topic at once, but a
	 * SUBSCRIBE can contain many topics at once, so this is one way to check
	 * them all. */
	for(i=0; i<qos_count; i++){
		printf("on_subscribe: %d:granted qos = %d\n", i, granted_qos[i]);
		if(granted_qos[i] <= 2){
			have_subscription = true;
		}
	}
	if(have_subscription == false){
		/* The broker rejected all of our subscriptions, we know we only sent
		 * the one SUBSCRIBE, so there is no point remaining connected. */
		fprintf(stderr, "Error: All subscriptions rejected.\n");
		mosquitto_disconnect(mosq);
	}
}


void send_luminosite(Luminosite *luminosite)
{
	char *string = NULL;
	cJSON *json_luminosite = cJSON_CreateObject();

	if (cJSON_AddStringToObject(json_luminosite, "capteur", luminosite->capteur) == NULL)
    {
		cJSON_Delete(json_luminosite);
		exit_error("erreur creation json", 2);
    }

    if (cJSON_AddNumberToObject(json_luminosite, "lux", luminosite->lux) == NULL)
    {
		cJSON_Delete(json_luminosite);
		exit_error("erreur creation json", 2);
    }

    string = cJSON_Print(json_luminosite);
    if (string == NULL)
    {
		exit_error("Failed to print luminosite.\n", 1);
    }

	cJSON_Delete(json_luminosite);

    // publie un message dans le sujet
    // parametres : client handle, message id, topic, length of message, message to be sent, QoS, retained
    mosquitto_publish(mosq, NULL, TOPIC_SEND, strlen(string)+1, (const void *)string, 0, false);
}


/* Callback called when the client receives a message. */
void on_message(struct mosquitto *mosq, void *obj, const struct mosquitto_message *msg)
{
	Luminosite mesure;

	/* This blindly prints the payload, but the payload can be anything so take care. */
	printf("on_message: topic=%s QOS=%d payload=%s\n", msg->topic, msg->qos, (char *)msg->payload);
	analyse_payload(&mesure, (char *)msg->payload);
	send_luminosite(&mesure);
}


int main(int argc, char *argv[])
{
	int rc;

	/* Required before calling other mosquitto functions */
	mosquitto_lib_init();

	/* Create a new client instance.
	 * id = NULL -> ask the broker to generate a client id for us
	 * clean session = true -> the broker should remove old sessions when we connect
	 * obj = NULL -> we aren't passing any of our private data for callbacks
	 */
	mosq = mosquitto_new(NULL, true, NULL);
	if(mosq == NULL){
		exit_error("Error: Out of memory.\n", 1);
	}

	/* Configure callbacks. This should be done before connecting ideally. */
	mosquitto_connect_callback_set(mosq, on_connect);
	mosquitto_subscribe_callback_set(mosq, on_subscribe);
	mosquitto_message_callback_set(mosq, on_message);

	/* Connect to broker on port 1883, with a keepalive of 60 seconds.
	 * This call makes the socket connection only, it does not complete the MQTT
	 * CONNECT/CONNACK flow, you should use mosquitto_loop_start() or
	 * mosquitto_loop_forever() for processing net traffic. */
	rc = mosquitto_connect(mosq, BROKER, BROKER_PORT, 60);
	if(rc != MOSQ_ERR_SUCCESS){
		mosquitto_destroy(mosq);
		exit_error(mosquitto_strerror(rc), 1);
	}

	mosquitto_loop_forever(mosq, -1, 1);	// Run the network loop in a blocking call

	mosquitto_lib_cleanup();

	return 0;
}
