# TP MQTT

## Objectif

Un capteur de température envoie sur le topic "sensors/bureau/temperature", une mesure de température toutes les 5 secondes, ainsi que certaines données incorrectes.

Vous devrez calculer une valeur normalisée de la temperature toutes les minutes et l'envoyer sur le topic "sensors/bureau/normalise".

Vous recevrez sur le topic "sensors/bureau/controle" la comparaison de votre calcul et de celui réalisé par le système.

Format des données du capteur :
```json
topic: sensors/bureau/temperature
payload: {
    'timestamp':999999, 
    'temperature':99.9
    }
```
- Filtrage des données: toutes données plus anciennes que 10 secondes et celles du futur doivent être ignorées.

Format des données normalisées :
```json
topic: sensors/bureau/normalise
payload: {
    'user_name': 'ABC', 
    'minute': 999, 
    'temperature': 99.9
    }
```
- Le champ minute représente le nombre de minutes depuis minuit
- Les données pour une minute sont triées par valeur.
- Le quart de données de valeur inférieures et le quart de valeurs supérieures sont ignorées
- Le résultat est la moyenne des valeurs restantes

Format des données de contrôle :
```json
topic: sensors/bureau/controle
payload: {
        'user_name': 'ABC',
        'minute': 999,
        'temperature': 99.9,
        'temp_check': 99.9,
        'status': 'status',
    }
```


## Configuration du broker

copier le fichier de configuration, puis insérer les paramètres correspondants à votre configuration:

```bash
cp client_c/config_dist.h client_c/config.h
```

Configurer les paramètres:
- adresse broker
- utilisateur
- mot de passe

## Exemples:

Exemples dans les sous dossiers de client_c/

## Utilitaires

- mqtt_subscribe.sh: script qui affiche les messages passant par le broker
