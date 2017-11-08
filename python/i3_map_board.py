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
disconnectedColor = Color(25*brightness,0,0) 							# red
offColor					= Color(0,0,25*brightness)							# blue
unknownColor			= Color(25*brightness,0,18*brightness)	# purple
onColor						= Color(0,25*brightness,0)							# green
#ledDark 					= Color(0,0,0)

class State(Enum):
	OFF = 1
	ON = 2
	DISCONNECTED = 3
	UNKNOWN = 4

# Map legend
strip.setPixelColor(1,onColor);
strip.setPixelColor(2,disconnectedColor);
strip.setPixelColor(3,offColor);
strip.setPixelColor(4,unknownColor);

# Devices are listed here in a dictionary with a number of keys
# 'topic' is the full MQTT topic to subscribe to/listen for
# 'ledNum' is the neopixel order number on the physical map
# 'itemState' is where the device's current state is stored
# 'onState' is the message payload corresponding to the device being on
# 'offState' is the message payload corresponding to the device being off
# 'offType' determines whether a device found to be "off" gets the state OFF or DISCONNECTED.
# 	offType is a little hacky, but it lets me treat stat and tele messages in a similar way.
#		*typically* stat and tele/../STATE messages result in the device being marked ON or OFF, while tele/../LWT messages result in the device being marked DISCONNECTED
#		But there are exceptions like the OpenEVSE which this allows for without having to hardcode 'stat means this' and 'tele means that'

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
{'topic': "tele/i3/commons/lights/snappleVending/LWT", 'ledNum': 32, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/accent/chandelier-01/LWT", 'ledNum': 37, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/accent/chandelier-02/LWT", 'ledNum': 72, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/classroom/sign/LWT", 'ledNum': 7, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/cnc/exhaust-fan/LWT", 'ledNum': 19, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/cnc/light/LWT", 'ledNum': 20, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/commons/disco/LWT", 'ledNum': 35, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/commons/east-ceiling-fans/LWT", 'ledNum': 27, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/commons/east-ceiling-fans/LWT", 'ledNum': 31, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/commons/openevse/state", 'ledNum': 12, 'itemState': State.UNKNOWN, 'onState':3, 'offState':1, 'offType': State.OFF},
{'topic': "tele/i3/inside/commons/openevse", 'ledNum': 12, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "disconnected", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/commons/south-vent/LWT", 'ledNum': 60, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/fablab/vent/LWT", 'ledNum': 59, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/infrastructure/compressor-valve/LWT", 'ledNum': 44, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/large-bathroom/light/LWT", 'ledNum': 64, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/large-bathroom/vent/LWT", 'ledNum': 65, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/001/LWT", 'ledNum': 14, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/002/LWT", 'ledNum': 16, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/003/LWT", 'ledNum': 17, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/004/LWT", 'ledNum': 18, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/005/LWT", 'ledNum': 13, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/006/LWT", 'ledNum': 30, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/007/LWT", 'ledNum': 29, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/008/LWT", 'ledNum': 28, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/009/LWT", 'ledNum': 26, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/010/LWT", 'ledNum': 33, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/011/LWT", 'ledNum': 34, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/012/LWT", 'ledNum': 36, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/013/LWT", 'ledNum': 38, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/014/LWT", 'ledNum': 39, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/015/LWT", 'ledNum': 61, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/016/LWT", 'ledNum': 52, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/017/LWT", 'ledNum': 49, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/018/LWT", 'ledNum': 48, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/019/LWT", 'ledNum': 45, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/020/LWT", 'ledNum': 62, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/021/LWT", 'ledNum': 56, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/022/LWT", 'ledNum': 54, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/023/LWT", 'ledNum': 51, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/024/LWT", 'ledNum': 50, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/025/LWT", 'ledNum': 46, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/026/LWT", 'ledNum': 47, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/027/LWT", 'ledNum': 63, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/028/LWT", 'ledNum': 15, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/029/LWT", 'ledNum': 21, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/030/LWT", 'ledNum': 22, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/031/LWT", 'ledNum': 24, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/032/LWT", 'ledNum': 23, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/033/LWT", 'ledNum': 42, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/034/LWT", 'ledNum': 41, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/035/LWT", 'ledNum': 40, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/036/LWT", 'ledNum': 55, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/lights/037/LWT", 'ledNum': 58, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/inside/machineShop/air-compressor/LWT", 'ledNum': 43, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/laserZone/ceilingFan/LWT", 'ledNum': 57, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/laserZone/ventFan/LWT", 'ledNum': 53, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/machineShop/fans/ceilingFan/LWT", 'ledNum': 25, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType': State.DISCONNECTED},
{'topic': "tele/i3/commons/lights/snappleVending/STATE", 'ledNum': 32, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/accent/chandelier-01/STATE", 'ledNum': 37, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/accent/chandelier-02/STATE", 'ledNum': 72, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/classroom/sign/STATE", 'ledNum': 7, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/cnc/exhaust-fan/STATE", 'ledNum': 19, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/cnc/light/STATE", 'ledNum': 20, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/commons/disco/STATE", 'ledNum': 35, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/commons/east-ceiling-fans/STATE", 'ledNum': 27, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/commons/east-ceiling-fans/STATE", 'ledNum': 31, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/commons/south-vent/STATE", 'ledNum': 60, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/fablab/vent/STATE", 'ledNum': 59, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/infrastructure/compressor-valve/STATE", 'ledNum': 44, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/large-bathroom/light/STATE", 'ledNum': 64, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/large-bathroom/vent/STATE", 'ledNum': 65, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/001/STATE", 'ledNum': 14, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/002/STATE", 'ledNum': 16, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/003/STATE", 'ledNum': 17, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/004/STATE", 'ledNum': 18, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/005/STATE", 'ledNum': 13, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/006/STATE", 'ledNum': 30, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/007/STATE", 'ledNum': 29, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/008/STATE", 'ledNum': 28, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/009/STATE", 'ledNum': 26, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/010/STATE", 'ledNum': 33, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/011/STATE", 'ledNum': 34, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/012/STATE", 'ledNum': 36, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/013/STATE", 'ledNum': 38, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/014/STATE", 'ledNum': 39, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/015/STATE", 'ledNum': 61, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/016/STATE", 'ledNum': 52, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/017/STATE", 'ledNum': 49, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/018/STATE", 'ledNum': 48, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/019/STATE", 'ledNum': 45, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/020/STATE", 'ledNum': 62, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/021/STATE", 'ledNum': 56, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/022/STATE", 'ledNum': 54, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/023/STATE", 'ledNum': 51, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/024/STATE", 'ledNum': 50, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/025/STATE", 'ledNum': 46, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/026/STATE", 'ledNum': 47, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/027/STATE", 'ledNum': 63, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/028/STATE", 'ledNum': 15, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/029/STATE", 'ledNum': 21, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/030/STATE", 'ledNum': 22, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/031/STATE", 'ledNum': 24, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/032/STATE", 'ledNum': 23, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/033/STATE", 'ledNum': 42, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/034/STATE", 'ledNum': 41, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/035/STATE", 'ledNum': 40, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/036/STATE", 'ledNum': 55, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/lights/037/STATE", 'ledNum': 58, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/inside/machineShop/air-compressor/STATE", 'ledNum': 43, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/laserZone/ceilingFan/STATE", 'ledNum': 57, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/laserZone/ventFan/STATE", 'ledNum': 53, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF},
{'topic': "tele/i3/machineShop/fans/ceilingFan/STATE", 'ledNum': 25, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType': State.OFF}
]

for item in deviceList:
	strip.setPixelColor(item['ledNum'],unknownColor)
strip.show()
time.sleep(wait_ms/1000.0)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.publish("tele/i3/inside/commons/map-board/INFO2", "online")

	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	for item in deviceList:
		print("subscribing to "+item['topic'])
		client.subscribe(item['topic'])

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print("received"+msg.topic+" "+msg.payload)
	for device in deviceList:
		# Match message topic to device, determine state of device
		# Coarse filtering for stat/tele
		if device['topic'][:4] == msg.topic[:4]:
			if device['topic'] == msg.topic:
				if device['onState'] in msg.payload:
					print(device['topic']+" is ON")
					device['itemState'] = State.ON
				elif device['offState'] in msg.payload:
					if device['offType'] == State.OFF:
						print(device['topic']+" is OFF")
						device['itemState'] = State.OFF
					elif device['offType'] == State.DISCONNECTED:
						print(device['topic']+" is DISCONNECTED")
						device['itemState'] = State.DISCONNECTED
			# Color the device LED		
			if device['itemState'] == State.OFF:
				strip.setPixelColor(device['ledNum'],offColor)
			elif device['itemState'] == State.ON:
				strip.setPixelColor(device['ledNum'],onColor)
			elif device['itemState'] == State.DISCONNECTED:
				strip.setPixelColor(device['ledNum'],disconnectedColor)			
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
