# Based on the example from https://pypi.python.org/pypi/paho-mqtt

import paho.mqtt.client as mqtt
import items_list

uniqueDevices = ["/i3/inside/commons/east-ceiling-fans/",
              "/i3/machineShop/fans/ceilingFan/",
              "/i3/laserZone/ceilingFan/",
              "/i3/laserZone/ventFan/",
              "/i3/inside/fablab/vent/",
              "/i3/inside/office-bathroom/light/",
              "/i3/inside/commons/bathroom-vent-fan/",
              "/i3/commons/lights/snappleVending/"]

subList = ["stat/i3/inside/lights/+/POWER",
          "tele/i3/inside/lights/+/LWT"]

pubList = ["cmnd/i3/inside/lights/all/POWER"]

for item in uniqueDevices:
  subList.append("stat"+item+"POWER")
  subList.append("tele"+item+"LWT")
  pubList.append("cmnd"+item+"POWER")

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.publish("tele/i3/inside/commons/map-board/INFO2", "online")

  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
  for item in subList:
    client.subscribe(item)

  for item in pubList:
    client.publish(item)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
  for device in deviceList:
    if device['topic'] in msg.topic
      #Check if status - POWER
      if msg.topic[:4] == "stat" and msg.topic[-5:] == "POWER":
        if str(msg.payload) == "ON" or str(msg.payload) == "1":
          device['itemState'] = State.ON
          print(device['topic']+" set to ON")
        elif str(msg.payload) == "OFF" or str(msg.payload) == "0":
          device['itemState'] = State.OFF
          print(device['topic']+" set to OFF")
      # Check if telemetry - LWT
      elif msg.topic[:4] == "tele" and msg.topic[-3:] == "LWT":
        if str(msg.payload) == "Offline":
          device['itemState'] = State.DISCONNECTED
          print(device['topic']+" set to DISCONNECTED")
      # set the device's LED to the appropriate color for its state here once I implement LEDs

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("10.13.0.22", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
