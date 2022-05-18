import paho.mqtt.client as mqtt
import string

def get_menu():
    print()
    print(f"client_id: {client_id}")
    print(f"Connexion: {client_cnx}")
    print("0-9: Initialiser un numéro de client")
    print("C: connexion")
    print("D: déconnexion")
    print("F: fin")
    print("H: Hello world")
    print("T: Tada")
    choix = input("Votre choix:")
    return choix

client_id = ""
client_cnx = False

choix = "0"
while choix != 'F':
    choix = get_menu()
    
    if choix in string.digits:
        client_id = "client" + choix

    elif choix == 'C':
        client = mqtt.Client(client_id)
        client.connect("127.0.0.1")
        client.publish("proc/connect", "connexion " + client_id)
        print("Connexion " + client_id)
        client_cnx = True

    elif choix == 'D':
        client.publish("proc/connect", "déconnexion " + client_id)
        client.disconnect()
        del client
        print("déconnexion " + client_id)
        client_cnx = False

    elif choix == 'H':
        client.publish("proc/connect", "Hello world " + client_id)
        print("Message hello world " + client_id)

    elif choix == 'T':
        client.publish("proc/connect", "Tada " + client_id)
        print("Message tada " + client_id)

    elif choix != 'F':
        print("Choix incorrect")


