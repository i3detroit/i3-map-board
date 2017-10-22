# Based on the example from https://pypi.python.org/pypi/paho-mqtt

import paho.mqtt.client as mqtt
from enum import Enum
import time
from neopixel import *

# LED strip configuration:
LED_COUNT      = 60      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

wait_ms = 50
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
strip.begin()

brightness = 3
ledRed = Color(25*brightness,0,0)
ledBlue = Color(0,0,25*brightness)
ledPurple = Color(25*brightness,0,18*brightness)
ledGreen = Color(0,25*brightness,0)
ledOff = Color(0,0,0)

class State(Enum):
  OFF = 1
  ON = 2
  DISCONNECTED = 3
  UNKNOWN = 4

openEVSEonlinetimer = 0

deviceList = [
{'topic': "/i3/inside/classroom/sign/", 'ledNum':5, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/commons/openevse/", 'ledNum':6, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/005/", 'ledNum':7, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/001/", 'ledNum':8, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/028/", 'ledNum':9, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/002/", 'ledNum':10, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/003/", 'ledNum':11, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/004/", 'ledNum':12, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/029/", 'ledNum':13, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/030/", 'ledNum':14, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/032/", 'ledNum':15, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/031/", 'ledNum':16, 'itemState': State.UNKNOWN},
{'topic': "/i3/machineShop/fans/ceilingFan/", 'ledNum':17, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/009/", 'ledNum':18, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/commons/east-ceiling-fans/", 'ledNum':19, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/008/", 'ledNum':20, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/007/", 'ledNum':21, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/006/", 'ledNum':22, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/commons/east-ceiling-fans/", 'ledNum':23, 'itemState': State.UNKNOWN},
{'topic': "/i3/commons/lights/snappleVending/", 'ledNum':24, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/010/", 'ledNum':25, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/011/", 'ledNum':26, 'itemState': State.UNKNOWN},
{'topic': "/i3/commons/discoBall/", 'ledNum':27, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/012/", 'ledNum':28, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/013/", 'ledNum':29, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/014/", 'ledNum':30, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/035/", 'ledNum':31, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/034/", 'ledNum':32, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/033/", 'ledNum':33, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/machineShop/air-compressor/", 'ledNum':34, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/019/", 'ledNum':35, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/025/", 'ledNum':36, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/026/", 'ledNum':37, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/018/", 'ledNum':38, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/017/", 'ledNum':39, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/024/", 'ledNum':40, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/023/", 'ledNum':41, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/016/", 'ledNum':42, 'itemState': State.UNKNOWN},
{'topic': "/i3/laserZone/ventFan/", 'ledNum':43, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/022/", 'ledNum':44, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/036/", 'ledNum':45, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/021/", 'ledNum':46, 'itemState': State.UNKNOWN},
{'topic': "/i3/laserZone/ceilingFan/", 'ledNum':47, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/037/", 'ledNum':48, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/fablab/vent/", 'ledNum':49, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/015/", 'ledNum':50, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/020/", 'ledNum':51, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/lights/027/", 'ledNum':52, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/office-bathroom/light/", 'ledNum':53, 'itemState': State.UNKNOWN},
{'topic': "/i3/inside/commons/bathroom-vent-fan/", 'ledNum':54, 'itemState': State.UNKNOWN}
]

uniqueDevices = ["/i3/inside/commons/east-ceiling-fans/",
              "/i3/machineShop/fans/ceilingFan/",
              "/i3/laserZone/ceilingFan/",
              "/i3/laserZone/ventFan/",
              "/i3/inside/fablab/vent/",
              "/i3/inside/office-bathroom/light/",
              "/i3/inside/commons/bathroom-vent-fan/",
              "/i3/commons/lights/snappleVending/",
              "/i3/commons/discoBall/",
              "/i3/inside/classroom/sign/",
              "/i3/inside/machineShop/air-compressor/"]

subList = ["stat/i3/inside/lights/+/POWER",
          "tele/i3/inside/lights/+/LWT",
          "tele/i3/inside/lights/+/STATE",
          "tele/i3/inside/commons/openevse/amp"]

pubList = ["cmnd/i3/inside/lights/east/POWER",
           "cmnd/i3/inside/lights/emergency/POWER"]

strip.setPixelColor(1,ledGreen);
strip.setPixelColor(2,ledRed);
strip.setPixelColor(3,ledBlue);
strip.setPixelColor(4,ledPurple);

for item in deviceList:
  strip.setPixelColor(item['ledNum'],ledPurple)
strip.show()
time.sleep(wait_ms/1000.0)

for item in uniqueDevices:
  subList.append("stat"+item+"POWER")
  subList.append("tele"+item+"LWT")
  subList.append("tele"+item+"STATE")
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
  global openEVSEonlinetimer
  for device in deviceList:
    if device['topic'] in msg.topic:
      #Check if status - POWER
      if msg.topic[:4] == "stat" and msg.topic[-5:] == "POWER":
        if str(msg.payload) == "ON" or str(msg.payload) == "1":
          device['itemState'] = State.ON
          print(device['topic']+" is ON")
        elif str(msg.payload) == "OFF" or str(msg.payload) == "0":
          device['itemState'] = State.OFF
          print(device['topic']+" is OFF")
      # Check if telemetry - LWT
      elif msg.topic[:4] == "tele" and msg.topic[-3:] == "LWT":
        if str(msg.payload) == "Offline":
          device['itemState'] = State.DISCONNECTED
          print(device['topic']+" is DISCONNECTED")
      # Check if telemetry - STATE
      elif msg.topic[:4] == "tele" and msg.topic[-5:] == "STATE":
        if "\"POWER\":\"OFF\"" in str(msg.payload):
          device['itemState'] = State.OFF
          print(device['topic']+" telemetry OFF")
        elif "\"POWER\":\"ON\"" in str(msg.payload):
          device['itemState'] = State.ON
          print(device['topic']+" telemetry ON")
      # Check if EV charger
      elif msg.topic[:4] == "tele" and msg.topic[-3:] == "amp":
        openEVSEonlinetimer = time.time()
        if int(msg.payload) == 0:
          device['itemState'] = State.OFF
          print("openEVSE on but not charging")
        elif int(msg.payload) > 0:
          device['itemState'] = State.ON
          print("openEVSE on and charging")
      
      # LED Coloring
      if (time.time()-openEVSEonlinetimer) > 45:
        deviceList[1]['itemState'] = State.DISCONNECTED
        strip.setPixelColor(deviceList[1]['ledNum'],ledRed)
      if device['itemState'] == State.OFF:
        strip.setPixelColor(device['ledNum'],ledBlue)
      elif device['itemState'] == State.ON:
        strip.setPixelColor(device['ledNum'],ledGreen)
      elif device['itemState'] == State.DISCONNECTED:
        strip.setPixelColor(device['ledNum'],ledRed)
      strip.show()
      time.sleep(wait_ms/1000.0)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("10.13.0.22", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
