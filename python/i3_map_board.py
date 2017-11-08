# Based on the example from https://pypi.python.org/pypi/paho-mqtt

import paho.mqtt.client as mqtt
from enum import Enum
import time
from neopixel import *

# LED strip configuration:
LED_COUNT      = 80      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
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
ledDisconnected = Color(25*brightness,0,0)
ledOff = Color(0,0,25*brightness)
ledUnkown = Color(25*brightness,0,18*brightness)
ledOn = Color(0,25*brightness,0)
ledOff = Color(0,0,0)

class State(Enum):
  OFF = 1
  ON = 2
  DISCONNECTED = 3
  UNKNOWN = 4

deviceList = [
{'topic': "stat/i3/classroom/glassDoor/lock", 'ledNum': 5, 'itemState': State.UNKNOWN, 'onState': "LOCKED", 'offState': "UNLOCKED", 'offType': State.OFF},
{'topic': "stat/i3/classroom/glassDoor/open", 'ledNum': 6, 'itemState': State.UNKNOWN, 'onState': "CLOSED", 'offState': "OPEN", 'offType': State.OFF},
{'topic': "stat/i3/commons/lights/snappleVending/POWER", 'ledNum': 32, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/accent/chandelier-01/POWER", 'ledNum': 37, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/accent/chandelier-02/POWER", 'ledNum': 72, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/classroom/sign/POWER", 'ledNum': 7, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/cnc/exhaust-fan/POWER", 'ledNum': 19, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/cnc/light/POWER", 'ledNum': 20, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/commons/disco/POWER", 'ledNum': 35, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/commons/east-ceiling-fans/POWER", 'ledNum': 27, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/commons/east-ceiling-fans/POWER", 'ledNum': 31, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/commons/garageDoor", 'ledNum': 11, 'itemState': State.UNKNOWN, 'onState': "LOCKED", 'offState': "UNLOCKED", 'offType': State.OFF},
{'topic': "stat/i3/inside/commons/south-vent/POWER", 'ledNum': 60, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/fablab/vent/POWER", 'ledNum': 59, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/infrastructure/compressor-valve/POWER", 'ledNum': 44, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/large-bathroom/light/POWER", 'ledNum': 64, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/large-bathroom/vent/POWER", 'ledNum': 65, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/001/POWER", 'ledNum': 14, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/002/POWER", 'ledNum': 16, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/003/POWER", 'ledNum': 17, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/004/POWER", 'ledNum': 18, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/005/POWER", 'ledNum': 13, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/006/POWER", 'ledNum': 30, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/007/POWER", 'ledNum': 29, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/008/POWER", 'ledNum': 28, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/009/POWER", 'ledNum': 26, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/010/POWER", 'ledNum': 33, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/011/POWER", 'ledNum': 34, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/012/POWER", 'ledNum': 36, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/013/POWER", 'ledNum': 38, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/014/POWER", 'ledNum': 39, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/015/POWER", 'ledNum': 61, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/016/POWER", 'ledNum': 52, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/017/POWER", 'ledNum': 49, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/018/POWER", 'ledNum': 48, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/019/POWER", 'ledNum': 45, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/020/POWER", 'ledNum': 62, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/021/POWER", 'ledNum': 56, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/022/POWER", 'ledNum': 54, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/023/POWER", 'ledNum': 51, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/024/POWER", 'ledNum': 50, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/025/POWER", 'ledNum': 46, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/026/POWER", 'ledNum': 47, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/027/POWER", 'ledNum': 63, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/028/POWER", 'ledNum': 15, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/029/POWER", 'ledNum': 21, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/030/POWER", 'ledNum': 22, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/031/POWER", 'ledNum': 24, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/032/POWER", 'ledNum': 23, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/033/POWER", 'ledNum': 42, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/034/POWER", 'ledNum': 41, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/035/POWER", 'ledNum': 40, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/036/POWER", 'ledNum': 55, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/lights/037/POWER", 'ledNum': 58, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/inside/machineShop/air-compressor/POWER", 'ledNum': 43, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/laserZone/ceilingFan/POWER", 'ledNum': 57, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/laserZone/ventFan/POWER", 'ledNum': 53, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "stat/i3/machineShop/fans/ceilingFan/POWER", 'ledNum': 25, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType': State.OFF},
{'topic': "tele/i3/commons/lights/snappleVending/LWT", 'ledNum': 32, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/accent/chandelier-01/LWT", 'ledNum': 37, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/accent/chandelier-02/LWT", 'ledNum': 72, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/classroom/sign/LWT", 'ledNum': 7, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/cnc/exhaust-fan/LWT", 'ledNum': 19, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/cnc/light/LWT", 'ledNum': 20, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/commons/disco/LWT", 'ledNum': 35, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/commons/east-ceiling-fans/LWT", 'ledNum': 27, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/commons/east-ceiling-fans/LWT", 'ledNum': 31, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/commons/openevse/state", 'ledNum': 12, 'itemState': State.UNKNOWN, 'onState':3, 'offState':1, 'offType': State.OFF},
{'topic': "tele/i3/inside/commons/openevse", 'ledNum': 12, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "disconnected", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/commons/south-vent/LWT", 'ledNum': 60, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/fablab/vent/LWT", 'ledNum': 59, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/infrastructure/compressor-valve/LWT", 'ledNum': 44, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/large-bathroom/light/LWT", 'ledNum': 64, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/large-bathroom/vent/LWT", 'ledNum': 65, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/001/LWT", 'ledNum': 14, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/002/LWT", 'ledNum': 16, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/003/LWT", 'ledNum': 17, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/004/LWT", 'ledNum': 18, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/005/LWT", 'ledNum': 13, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/006/LWT", 'ledNum': 30, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/007/LWT", 'ledNum': 29, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/008/LWT", 'ledNum': 28, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/009/LWT", 'ledNum': 26, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/010/LWT", 'ledNum': 33, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/011/LWT", 'ledNum': 34, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/012/LWT", 'ledNum': 36, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/013/LWT", 'ledNum': 38, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/014/LWT", 'ledNum': 39, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/015/LWT", 'ledNum': 61, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/016/LWT", 'ledNum': 52, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/017/LWT", 'ledNum': 49, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/018/LWT", 'ledNum': 48, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/019/LWT", 'ledNum': 45, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/020/LWT", 'ledNum': 62, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/021/LWT", 'ledNum': 56, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/022/LWT", 'ledNum': 54, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/023/LWT", 'ledNum': 51, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/024/LWT", 'ledNum': 50, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/025/LWT", 'ledNum': 46, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/026/LWT", 'ledNum': 47, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/027/LWT", 'ledNum': 63, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/028/LWT", 'ledNum': 15, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/029/LWT", 'ledNum': 21, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/030/LWT", 'ledNum': 22, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/031/LWT", 'ledNum': 24, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/032/LWT", 'ledNum': 23, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/033/LWT", 'ledNum': 42, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/034/LWT", 'ledNum': 41, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/035/LWT", 'ledNum': 40, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/036/LWT", 'ledNum': 55, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/037/LWT", 'ledNum': 58, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/machineShop/air-compressor/LWT", 'ledNum': 43, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/laserZone/ceilingFan/LWT", 'ledNum': 57, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/laserZone/ventFan/LWT", 'ledNum': 53, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/machineShop/fans/ceilingFan/LWT", 'ledNum': 25, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType': State.DISCONNECTED}
]

strip.setPixelColor(1,ledGreen);
strip.setPixelColor(2,ledRed);
strip.setPixelColor(3,ledBlue);
strip.setPixelColor(4,ledPurple);

for item in deviceList:
  strip.setPixelColor(item['ledNum'],ledPurple)
strip.show()
time.sleep(wait_ms/1000.0)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.publish("tele/i3/inside/commons/map-board/INFO2", "online")

  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
  for item in deviceList:
    client.subscribe(item['topic'])

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
  for device in deviceList:
    if device['topic'] == msg.topic:
    	if device['onState'] == msg.payload:
    		print(device['topic']+" is ON")
    	elif device['offState'] == msg.payload:
    		if device['offType'] == State.OFF:
    			print(device['topic']+" is OFF")
    		elif device['offType'] == State.DISCONNECTED:
    			print(device['topic']+" is DISCONNECTED")
    			
    			
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
