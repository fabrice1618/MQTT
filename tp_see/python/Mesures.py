from datetime import datetime


def minutes_depuis_minuit(timestamp):
    # Convertir le timestamp en objet datetime
    dt = datetime.fromtimestamp(timestamp)
    
    # Créer un objet datetime représentant minuit du même jour
    minuit = datetime.combine(dt.date(), datetime.min.time())
    
    # Calculer la différence en minutes entre le timestamp et minuit
    diff = dt - minuit
    minutes = int(diff.total_seconds() / 60)
    
    return minutes

class Mesures:
    _mesures = None

    @classmethod
    def clear(cls):
        cls._mesures = list()

    @classmethod
    def values(cls):
        return cls._mesures

    @classmethod
    def stocker(cls, payload):

        if not 'timestamp' in payload or \
           not 'temperature' in payload:
            raise ValueError("Mesure structure incorrecte")

        mesure = {
            "minute": minutes_depuis_minuit(payload['timestamp']),
            "timestamp": payload['timestamp'], 
            "temperature": payload['temperature'], 
            }

        cls._mesures.append(mesure)

        # Filtrer les mesures pour ne conserver que 2 minutes
        minute_filtre = minutes_depuis_minuit( datetime.now().timestamp() ) - 2
        cls._mesures = [x for x in cls._mesures if x['minute'] >= minute_filtre] 

    @classmethod
    def temperature_normalise(cls, minute):
        # Filtrer les mesures, conserver celles de la minute demandée
        temperatures = [x['temperature'] for x in cls._mesures if x['minute'] == minute] 
        if len(temperatures) == 0:
            return None
        temperatures.sort()
        ignore_val = len(temperatures) // 4
        temperatures = temperatures[ignore_val:-ignore_val]
        temp_moyenne = round(sum(temperatures) / len(temperatures), 1)
        return temp_moyenne

