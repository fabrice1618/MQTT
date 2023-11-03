/*
 * Traitement des données provenant des capteurs et envoi sur le topic datastore/luminosite
 */

#include <mosquitto.h>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "../config.h"
#include "../cJSON.h"
#include "Luminosite.h"

#define TOPIC_SEND "datastore/luminosite"
#define TOPIC_RECEIVE "sensor/luminosite"

// Variables globales
struct mosquitto *mosq;

/* Callback called when the client receives a CONNACK message from the broker. */
void on_connect(struct mosquitto *mosq, void *obj, int reason_code)
{
	int rc;

	printf("on_connect: %s\n", mosquitto_connack_string(reason_code));
	if(0 != reason_code){
		mosquitto_disconnect(mosq);
        std::cerr << "connection fails" << std::endl;
        throw 1;
	}

	/* Making subscriptions in the on_connect() callback */
	rc = mosquitto_subscribe(mosq, NULL, TOPIC_RECEIVE, 1);
	if(MOSQ_ERR_SUCCESS != rc){
		mosquitto_disconnect(mosq);
        std::cerr << "Error subscribing: " << mosquitto_strerror(rc) << std::endl;
        throw 1;
	}
}

/* Callback called when the broker sends a SUBACK in response to a SUBSCRIBE. */
void on_subscribe(struct mosquitto *mosq, void *obj, int mid, int qos_count, const int *granted_qos)
{
	int i;
	bool have_subscription = false;

	for(i=0; i<qos_count; i++){
		printf("on_subscribe: %d:granted qos = %d\n", i, granted_qos[i]);
		if(granted_qos[i] <= 2){
			have_subscription = true;
		}
	}
	if(have_subscription == false){
		/* The broker rejected all of our subscriptions */
		mosquitto_disconnect(mosq);
        std::cerr << "Error: All subscriptions rejected." << std::endl;
        throw 1;
	}
}

/* Callback called when the client receives a message. */
void on_message(struct mosquitto *mosq, void *obj, const struct mosquitto_message *msg)
{
	Luminosite luminosite;

	printf("on_message: topic=%s QOS=%d payload=%s\n", msg->topic, msg->qos, (char *)msg->payload);

	if (strcmp(msg->topic, TOPIC_RECEIVE) == 0) {
		luminosite.from_JSON((char *)msg->payload);
		mosquitto_publish(mosq, NULL, TOPIC_SEND, luminosite.message_len(), luminosite.message(), 0, false);
	}
}

int main(int argc, char *argv[])
{
	int rc;

	mosquitto_lib_init();

	/* Create a new client instance. */
	mosq = mosquitto_new(NULL, true, NULL);
	if(NULL == mosq){
        std::cerr << "Error: Out of memory." << std::endl;
        throw 1;
	}

	/* Configure callbacks. This should be done before connecting ideally. */
	mosquitto_connect_callback_set(mosq, on_connect);
	mosquitto_subscribe_callback_set(mosq, on_subscribe);
	mosquitto_message_callback_set(mosq, on_message);

	/* Connect to broker on port 1883, with a keepalive of 60 seconds. */
	rc = mosquitto_connect(mosq, BROKER, BROKER_PORT, 60);
	if(MOSQ_ERR_SUCCESS != rc){
		mosquitto_destroy(mosq);
        std::cerr << mosquitto_strerror(rc) << std::endl;
        throw 1;
	}

	mosquitto_loop_forever(mosq, -1, 1);	// Run the network loop in a blocking call

	mosquitto_lib_cleanup();

	return 0;
}
