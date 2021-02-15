import configparser
import paho.mqtt.client as mqtt
import ssl
import time
import os
########################################################################
###      Utilizzo "DjangoREST" settings e modelli
########################################################################
import DjangoREST
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoREST.settings")
import django
django.setup()
from record import models
########################################################################
# leggo la configurazione
config = configparser.ConfigParser()
config.read('config.ini')

# callback per la ricezione dei messaggi
def mqtt_message(message):
    print(message)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True  # set flag
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)


mqtt.Client.connected_flag = False
client = mqtt.Client(config.get('mqtt_broker', 'client_id'))
client.username_pw_set(config.get('mqtt_broker', 'user'), config.get('mqtt_broker', 'password'))
client.tls_set(ca_certs=None,
               certfile=None,
               keyfile=None,
               cert_reqs=ssl.CERT_NONE,
               tls_version=ssl.PROTOCOL_TLS,
               ciphers=None)
client.connect_async(config.get("mqtt_broker", "host"), port=8884, keepalive=60, bind_address='')
client.on_connect = on_connect
client.on_message = mqtt_message
client.loop_start()
print(f'host: {config.get("mqtt_broker", "host")}')
client.subscribe(config.get('mqtt_broker', 'topic'))
while not client.connected_flag:  # wait in loop
    print("In wait loop")
    time.sleep(3)
print("in Main Loop")

client.loop_forever()  # Stop loop
#client.disconnect()  # disconnect
