import paho.mqtt.client as mqtt
import string

def print_menu():
    print()
    print("0-9: Message numérique")
    print("H: Hello world")
    print("Q: Quitter")

def get_menu():
    choix = None

    while choix is None:
        print_menu()
        saisie = input("Votre choix: ")

        if saisie in string.digits:
            choix = int(saisie)
        elif saisie.upper() in ['H', 'Q']:
            choix = saisie.upper()
        else:
            print("Erreur choix incorrect")

    return choix

def main():
    client = mqtt.Client("client")
    client.connect("mosquitto")

    choix = None
    while choix != 'Q':
        choix = get_menu()
        
        if isinstance(choix, int):
            client.publish("sensor/client", str(choix))
            print("> sending number", choix)

        elif choix == 'H':
            client.publish("sensor/hello", "Hello world ")
            print("> sending hello world")


if __name__ == '__main__':
    main()
