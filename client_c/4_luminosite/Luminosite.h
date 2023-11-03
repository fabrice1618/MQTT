#pragma once
#include <string>

#define NOMBRE_MESURES 8

class Luminosite
{
private:
    std::string m_message;
    int m_lux;
    std::string m_capteur;
    int tab_mesure[NOMBRE_MESURES];

public:
    Luminosite();
    void from_JSON(char *payload);
    int message_len();
    const char* message();
private:
    void parse_JSON(char *payload);
    void compute_lux();
    void to_JSON();
};
	
