#include <stdio.h> 
#include "cJSON.h"

int main() { 
    // open the file 
    FILE *fp = fopen("data.json", "r"); 
    if (fp == NULL) { 
        printf("Error: Unable to open the file.\n"); 
        return 1; 
    } 
  
    // read the file contents into a string 
    char buffer[1024]; 
    int len = fread(buffer, 1, sizeof(buffer), fp); 
    fclose(fp); 

	// parse the JSON data 
	cJSON *json = cJSON_Parse(buffer); 
	if (json == NULL) { 
		const char *error_ptr = cJSON_GetErrorPtr(); 
		if (error_ptr != NULL) { 
			printf("Error: %s\n", error_ptr); 
		} 
		cJSON_Delete(json); 
		return 1; 
	} 

	// access the JSON data 
	cJSON *capteur = cJSON_GetObjectItemCaseSensitive(json, "capteur"); 
	if (cJSON_IsString(capteur) && (capteur->valuestring != NULL)) { 
		printf("capteur: %s\n", capteur->valuestring); 
	} 

    const cJSON *mesure = NULL;
    const cJSON *mesures = NULL;

    mesures = cJSON_GetObjectItemCaseSensitive(json, "mesures");
    cJSON_ArrayForEach(mesure, mesures)
    {
        if (!cJSON_IsNumber(mesure))
        {
            printf("n'est pas un nombre\n");
        } else {
            printf("nombre: %d\n", (int)mesure->valuedouble);
        }

    }


	// delete the JSON object 
	cJSON_Delete(json); 
	return 0; 
}
