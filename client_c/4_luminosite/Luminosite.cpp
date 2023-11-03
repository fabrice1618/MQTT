#include <cstring>
#include <iostream>
#include "Luminosite.h"
#include "../cJSON.h"

#define VAL_MINI 0
#define VAL_MAXI 65535

#define ECHANGE(x, y) { int t = (x); (x) = (y); (y) = t; }

// Définition
Luminosite::Luminosite()
{
    m_message = "";
    m_capteur = "";
    m_lux = 0;

	for(int i = 0; i < NOMBRE_MESURES; i++) {
		tab_mesure[i] = 0;
	}
}

void Luminosite::from_JSON(char *msg_payload)
{
    parse_JSON(msg_payload);
    compute_lux();
    to_JSON();
}

void Luminosite::parse_JSON(char *msg_payload)
{
	// parse the JSON data 
	cJSON *json = cJSON_Parse(msg_payload); 
	if (json == NULL) { 
		const char *error_ptr = cJSON_GetErrorPtr();
		cJSON_Delete(json);
        std::cerr << error_ptr << std::endl;
        throw 1;
	} 

	// access the JSON data 
	cJSON *capteur = cJSON_GetObjectItemCaseSensitive(json, "capteur"); 
	if (cJSON_IsString(capteur) && (capteur->valuestring != NULL)) { 
        m_capteur = std::string(capteur->valuestring);
	} 

    const cJSON *mesure = NULL;
    const cJSON *mesures = NULL;
	int indice = 0;

    mesures = cJSON_GetObjectItemCaseSensitive(json, "mesures");
    cJSON_ArrayForEach(mesure, mesures)
    {
        if (cJSON_IsNumber(mesure) && (indice < NOMBRE_MESURES)) {
			tab_mesure[indice++] = (int)mesure->valuedouble;
        }
    }

	// delete the JSON object 
	cJSON_Delete(json); 
}

void Luminosite::compute_lux()
{
    int i;
    int mini0 = VAL_MAXI + 1;
    int mini1 = VAL_MAXI + 1;
    int maxi0 = VAL_MINI - 1;
    int maxi1 = VAL_MINI - 1;
    int total = 0;
    int nb_val = 0;

    for( i = 0; i < 8; i++) {
        if ( tab_mesure[i] >= VAL_MINI && tab_mesure[i] <= VAL_MAXI) {
            total += tab_mesure[i];
            nb_val++;

            // Si valeur capteur < mini
            if ( mini0 > tab_mesure[i] ) {
                mini0 = tab_mesure[i];
                if ( mini0 < mini1 ) {
                    ECHANGE( mini0, mini1 );
                }
            }

            // Si valeur capteur > maxi
            if ( maxi0 < tab_mesure[i] ) {
                maxi0 = tab_mesure[i];
                if (maxi0 > maxi1) {
                    ECHANGE( maxi0, maxi1 );
                }
            }
        }
    }

    if (nb_val - 4 > 0)
        m_lux = (total - mini0 - mini1 - maxi0 - maxi1) / (nb_val - 4);
}

void Luminosite::to_JSON()
{
	char *json_string = NULL;
	cJSON *json_luminosite = cJSON_CreateObject();

	if (cJSON_AddStringToObject(json_luminosite, "capteur", m_capteur.c_str()) == NULL) {
		cJSON_Delete(json_luminosite);
        std::cerr << "erreur creation json" << std::endl;
        throw 2;
    }

    if (cJSON_AddNumberToObject(json_luminosite, "lux", m_lux) == NULL) {
		cJSON_Delete(json_luminosite);
        std::cerr << "erreur creation json" << std::endl;
        throw 2;
    }

    json_string = cJSON_Print(json_luminosite);
    if (json_string == NULL) {
	    std::cerr << "Failed to print luminosite." << std::endl;
        throw 1;
    }

    m_message = std::string(json_string);

	cJSON_Delete(json_luminosite);
}

int Luminosite::message_len()
{
    return m_message.size() + 1;
}

const char* Luminosite::message()
{
    const char *message_payload = m_message.c_str();

    return message_payload;
}

