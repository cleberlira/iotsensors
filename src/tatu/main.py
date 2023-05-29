import paho.mqtt.client as mqtt
import json
import tatu

from time import sleep

#You don't need to change this file. Just change sensors.py and config.json

topicPrefix = "dev/"

def on_connect(mqttc, obj, flags, rc):
    topic = topicPrefix + obj["deviceName"] + "/#"
    print("Topic device subscribed: " + topic)
    mqttc.subscribe(topic)

def on_message(mqttc, obj, msg):
    if "RES" not in msg.topic:
    	tatu.main(obj, msg)

def on_disconnect(mqttc, obj, rc):
	print("disconnected!")
	exit()

while True:
	with open('config.json') as f:
		data = json.load(f)
	
	mqttBroker = data["mqttBroker"]
	mqttPort = data["mqttPort"]
	mqttUsername = data["mqttUsername"]
	mqttPassword = data["mqttPassword"]
	deviceName = data["deviceName"]

	sub_client = mqtt.Client(deviceName + "_sub")

	sub_client.username_pw_set(mqttUsername, mqttPassword)
	sub_client.user_data_set(data)
	sub_client.on_connect = on_connect
	sub_client.on_message = on_message
	sub_client.on_disconnect = on_disconnect

	try:
		sub_client.connect(mqttBroker, mqttPort, 60)
		sub_client.loop_forever()
	except:
		print ("Broker unreachable on " + mqttBroker + " URL!")
		f.close()
		sleep(5)

