# Based on the example from https://pypi.python.org/pypi/paho-mqtt

import paho.mqtt.client as mqtt
from enum import Enum
import time
from neopixel import *

# LED strip configuration:
LED_COUNT = 100      # Number of LED pixels.
LED_PIN = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

wait_ms = 50
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
strip.begin()

brightness = 4
disconnectedColor = Color(25 * brightness, 0, 0)                            # red
alwaysOnColor = Color(25 * brightness, 10 * brightness, 0)  # amber
unknownColor = Color(25 * brightness, 0, 18 * brightness)  # purple
onColor = Color(0, 25 * brightness, 0)                          # green
offColor = Color(0, 0, 25 * brightness)                         # blue
# ledDark = Color(0,0,0)


class State(Enum):
    OFF = 1
    ON = 2
    DISCONNECTED = 3
    UNKNOWN = 4


# Map legend
strip.setPixelColor(1, unknownColor)
strip.setPixelColor(2, onColor)
strip.setPixelColor(3, alwaysOnColor)
strip.setPixelColor(4, offColor)
strip.setPixelColor(5, disconnectedColor)

# Devices are listed here in a dictionary with a number of keys
# 'topic' is the full MQTT topic to subscribe to/listen for
# 'ledNum' is the neopixel order number on the physical map
# 'itemState' is where the device's current state is stored
# 'onState' is the message payload corresponding to the device being on
# 'offState' is the message payload corresponding to the device being off
# 'offType' determines whether a device found to be "off" gets the state OFF or DISCONNECTED.
#   offType is a little hacky, but it lets me treat stat and tele messages in a similar way.
#   *typically* stat and tele/../STATE messages result in the device being marked ON or OFF, while tele/../LWT messages result in the device being marked DISCONNECTED
#   But there are exceptions like the OpenEVSE which this allows for without having to hardcode 'stat means this' and 'tele means that'

deviceList = [
    {'topic': "stat/i3/inside/classroom/glass-door/lock", 'ledNum':6, 'itemState': State.UNKNOWN, 'onState': "LOCKED", 'offState': "UNLOCKED", 'offType':State.OFF, 'alwaysOn':True},
    {'topic': "stat/i3/inside/classroom/glass-door/open", 'ledNum':7, 'itemState': State.UNKNOWN, 'onState': "CLOSED", 'offState': "OPEN", 'offType':State.OFF, 'alwaysOn':True},
    {'topic': "stat/i3/inside/commons/snapple-vending-light/POWER", 'ledNum':33, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':True},
    {'topic': "stat/i3/inside/accent/chandelier-01/POWER", 'ledNum':38, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/accent/chandelier-02/POWER", 'ledNum':73, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/classroom/sign/POWER", 'ledNum':8, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':None},
    {'topic': "stat/i3/inside/cnc/vent/POWER", 'ledNum':20, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/cnc/light/POWER", 'ledNum':21, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/commons/disco/POWER", 'ledNum':36, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/commons/ceiling-fans/POWER", 'ledNum':28, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/commons/ceiling-fans/POWER", 'ledNum':32, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/commons/garage-door/lock", 'ledNum':12, 'itemState': State.UNKNOWN, 'onState': "LOCKED", 'offState': "UNLOCKED", 'offType':State.OFF, 'alwaysOn':True},
    {'topic': "stat/i3/inside/commons/south-vent/POWER", 'ledNum':61, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/fablab/chiller/POWER", 'ledNum':60, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/infrastructure/compressor-valve/POWER", 'ledNum':45, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/large-bathroom/light/POWER", 'ledNum':65, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/large-bathroom/vent/POWER", 'ledNum':66, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/001/POWER", 'ledNum':15, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/002/POWER", 'ledNum':17, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/003/POWER", 'ledNum':18, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/004/POWER", 'ledNum':19, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/005/POWER", 'ledNum':14, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/006/POWER", 'ledNum':31, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/007/POWER", 'ledNum':30, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/008/POWER", 'ledNum':29, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/009/POWER", 'ledNum':27, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/010/POWER", 'ledNum':34, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/011/POWER", 'ledNum':35, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/012/POWER", 'ledNum':37, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/013/POWER", 'ledNum':39, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/014/POWER", 'ledNum':40, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/015/POWER", 'ledNum':62, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/016/POWER", 'ledNum':53, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/017/POWER", 'ledNum':50, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/018/POWER", 'ledNum':49, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/019/POWER", 'ledNum':46, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/020/POWER", 'ledNum':63, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/021/POWER", 'ledNum':57, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/022/POWER", 'ledNum':55, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/023/POWER", 'ledNum':52, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/024/POWER", 'ledNum':51, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/025/POWER", 'ledNum':47, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/026/POWER", 'ledNum':48, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/027/POWER", 'ledNum':64, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':True},
    {'topic': "stat/i3/inside/lights/028/POWER", 'ledNum':16, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/029/POWER", 'ledNum':22, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/030/POWER", 'ledNum':23, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/031/POWER", 'ledNum':25, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/032/POWER", 'ledNum':24, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/033/POWER", 'ledNum':43, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/034/POWER", 'ledNum':42, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/035/POWER", 'ledNum':41, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/036/POWER", 'ledNum':56, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/037/POWER", 'ledNum':59, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/infrastructure/air-compressor/POWER", 'ledNum':44, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/laser-zone/ceiling-fan/POWER", 'ledNum':58, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/laser-zone/vent-fan/POWER", 'ledNum':54, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/machine-shop/ceiling-fan/POWER", 'ledNum':26, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/media-lab/lights/POWER", 'ledNum':71, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/commons/openevse/state", 'ledNum':13, 'itemState': State.UNKNOWN, 'onState':3, 'offState':1, 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/commons/openevse", 'ledNum':13, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "disconnected", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/commons/snapple-vending-light/LWT", 'ledNum':33, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':True},
    {'topic': "tele/i3/inside/accent/chandelier-01/LWT", 'ledNum':38, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/accent/chandelier-02/LWT", 'ledNum':73, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/classroom/sign/LWT", 'ledNum':8, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':None},
    {'topic': "tele/i3/inside/cnc/vent/LWT", 'ledNum':20, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/cnc/light/LWT", 'ledNum':21, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/commons/disco/LWT", 'ledNum':36, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/commons/ceiling-fans/LWT", 'ledNum':28, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/commons/ceiling-fans/LWT", 'ledNum':32, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/commons/south-vent/LWT", 'ledNum':61, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/fablab/chiller/LWT", 'ledNum':60, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/infrastructure/compressor-valve/LWT", 'ledNum':45, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/large-bathroom/light/LWT", 'ledNum':65, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/large-bathroom/vent/LWT", 'ledNum':66, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/001/LWT", 'ledNum':15, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/002/LWT", 'ledNum':17, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/003/LWT", 'ledNum':18, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/004/LWT", 'ledNum':19, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/005/LWT", 'ledNum':14, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/006/LWT", 'ledNum':31, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/007/LWT", 'ledNum':30, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/008/LWT", 'ledNum':29, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/009/LWT", 'ledNum':27, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/010/LWT", 'ledNum':34, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/011/LWT", 'ledNum':35, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/012/LWT", 'ledNum':37, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/013/LWT", 'ledNum':39, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/014/LWT", 'ledNum':40, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/015/LWT", 'ledNum':62, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/016/LWT", 'ledNum':53, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/017/LWT", 'ledNum':50, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/018/LWT", 'ledNum':49, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/019/LWT", 'ledNum':46, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/020/LWT", 'ledNum':63, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/021/LWT", 'ledNum':57, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/022/LWT", 'ledNum':55, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/023/LWT", 'ledNum':52, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/024/LWT", 'ledNum':51, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/025/LWT", 'ledNum':47, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/026/LWT", 'ledNum':48, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/027/LWT", 'ledNum':64, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':True},
    {'topic': "tele/i3/inside/lights/028/LWT", 'ledNum':16, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/029/LWT", 'ledNum':22, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/030/LWT", 'ledNum':23, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/031/LWT", 'ledNum':25, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/032/LWT", 'ledNum':24, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/033/LWT", 'ledNum':43, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/034/LWT", 'ledNum':42, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/035/LWT", 'ledNum':41, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/036/LWT", 'ledNum':56, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/037/LWT", 'ledNum':59, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/infrastructure/air-compressor/LWT", 'ledNum':44, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/laser-zone/ceiling-fan/LWT", 'ledNum':58, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/laser-zone/vent-fan/LWT", 'ledNum':54, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/machine-shop/ceiling-fan/LWT", 'ledNum':26, 'itemState': State.UNKNOWN, 'onState': "placeholder", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/media-lab/lights/LWT", 'ledNum':71, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/commons/snapple-vending-light/STATE", 'ledNum':33, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':True},
    {'topic': "tele/i3/inside/accent/chandelier-01/STATE", 'ledNum':38, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/accent/chandelier-02/STATE", 'ledNum':73, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/classroom/sign/STATE", 'ledNum':8, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':None},
    {'topic': "tele/i3/inside/cnc/vent/STATE", 'ledNum':20, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/cnc/light/STATE", 'ledNum':21, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/commons/disco/STATE", 'ledNum':36, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/commons/ceiling-fans/STATE", 'ledNum':28, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/commons/ceiling-fans/STATE", 'ledNum':32, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/commons/south-vent/STATE", 'ledNum':61, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/fablab/chiller/STATE", 'ledNum':60, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/infrastructure/compressor-valve/STATE", 'ledNum':45, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/large-bathroom/light/STATE", 'ledNum':65, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/large-bathroom/vent/STATE", 'ledNum':66, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/001/STATE", 'ledNum':15, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/002/STATE", 'ledNum':17, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/003/STATE", 'ledNum':18, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/004/STATE", 'ledNum':19, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/005/STATE", 'ledNum':14, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/006/STATE", 'ledNum':31, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/007/STATE", 'ledNum':30, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/008/STATE", 'ledNum':29, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/009/STATE", 'ledNum':27, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/010/STATE", 'ledNum':34, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/011/STATE", 'ledNum':35, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/012/STATE", 'ledNum':37, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/013/STATE", 'ledNum':39, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/014/STATE", 'ledNum':40, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/015/STATE", 'ledNum':62, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/016/STATE", 'ledNum':53, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/017/STATE", 'ledNum':50, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/018/STATE", 'ledNum':49, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/019/STATE", 'ledNum':46, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/020/STATE", 'ledNum':63, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/021/STATE", 'ledNum':57, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/022/STATE", 'ledNum':55, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/023/STATE", 'ledNum':52, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/024/STATE", 'ledNum':51, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/025/STATE", 'ledNum':47, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/026/STATE", 'ledNum':48, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/027/STATE", 'ledNum':64, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':True},
    {'topic': "tele/i3/inside/lights/028/STATE", 'ledNum':16, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/029/STATE", 'ledNum':22, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/030/STATE", 'ledNum':23, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/031/STATE", 'ledNum':25, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/032/STATE", 'ledNum':24, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/033/STATE", 'ledNum':43, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/034/STATE", 'ledNum':42, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/035/STATE", 'ledNum':41, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/036/STATE", 'ledNum':56, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/lights/037/STATE", 'ledNum':59, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/infrastructure/air-compressor/STATE", 'ledNum':44, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/laser-zone/ceiling-fan/STATE", 'ledNum':58, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/laser-zone/vent-fan/STATE", 'ledNum':54, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/machine-shop/ceiling-fan/STATE", 'ledNum':26, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/media-lab/lights/STATE", 'ledNum':71, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/commons/paint-box/POWER", 'ledNum':74, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/commons/paint-box/LWT", 'ledNum':74, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/commons/paint-box/STATE", 'ledNum':74, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/fablab/vent/POWER", 'ledNum':76, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/fablab/vent/LWT", 'ledNum':76, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/fablab/vent/STATE", 'ledNum':76, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/lights/039/POWER", 'ledNum':77, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':True},
    {'topic': "tele/i3/inside/lights/039/LWT", 'ledNum':77, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':True},
    {'topic': "tele/i3/inside/lights/039/STATE", 'ledNum':77, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':True},
    {'topic': "stat/i3/inside/lights/038/POWER", 'ledNum':80, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':True},
    {'topic': "tele/i3/inside/lights/038/LWT", 'ledNum':80, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':True},
    {'topic': "tele/i3/inside/lights/038/STATE", 'ledNum':80, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':True},
    {'topic': "stat/i3/inside/lights/040/POWER", 'ledNum':85, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':True},
    {'topic': "tele/i3/inside/lights/040/LWT", 'ledNum':85, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':True},
    {'topic': "tele/i3/inside/lights/040/STATE", 'ledNum':85, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':True},
    {'topic': "stat/i3/inside/craftroom/light/POWER", 'ledNum':10, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/craftroom/light/LWT", 'ledNum':10, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/craftroom/light/STATE", 'ledNum':10, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/elab/light/POWER", 'ledNum':81, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/elab/light/LWT", 'ledNum':81, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/elab/light/STATE", 'ledNum':81, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/elab/light/POWER", 'ledNum':82, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/elab/light/LWT", 'ledNum':82, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/elab/light/STATE", 'ledNum':82, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/elab/light/POWER", 'ledNum':67, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/elab/light/LWT", 'ledNum':67, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/elab/light/STATE", 'ledNum':67, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/hallway/light/POWER", 'ledNum':68, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/hallway/light/POWER", 'ledNum':69, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/hallway/light/LWT", 'ledNum':68, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/hallway/light/LWT", 'ledNum':69, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/hallway/light/STATE", 'ledNum':68, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/hallway/light/STATE", 'ledNum':69, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/laser-zone/bumblebee/laser/POWER", 'ledNum':83, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/laser-zone/bumblebee/laser/LWT", 'ledNum':83, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/laser-zone/bumblebee/laser/STATE", 'ledNum':83, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/laser-zone/wolverine/laser/POWER", 'ledNum':84, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/laser-zone/wolverine/laser/LWT", 'ledNum':84, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/laser-zone/wolverine/laser/STATE", 'ledNum':84, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "stat/i3/inside/small-bathroom/light/POWER", 'ledNum':70, 'itemState': State.UNKNOWN, 'onState': "ON", 'offState': "OFF", 'offType':State.OFF, 'alwaysOn':False},
    {'topic': "tele/i3/inside/small-bathroom/light/LWT", 'ledNum':70, 'itemState': State.UNKNOWN, 'onState': "Online", 'offState': "Offline", 'offType':State.DISCONNECTED, 'alwaysOn':False},
    {'topic': "tele/i3/inside/small-bathroom/light/STATE", 'ledNum':70, 'itemState': State.UNKNOWN, 'onState': "\"POWER\":\"ON\"", 'offState': "\"POWER\":\"OFF\"", 'offType':State.OFF, 'alwaysOn':False}
]

pubList = [
    "cmnd/i3/inside/classroom/glass-door/lock",
    "cmnd/i3/inside/classroom/glass-door/open",
    "cmnd/i3/inside/commons/snapple-vending-light/POWER",
    "cmnd/i3/inside/accent/chandelier-01/POWER",
    "cmnd/i3/inside/accent/chandelier-02/POWER",
    "cmnd/i3/inside/classroom/sign/POWER",
    "cmnd/i3/inside/cnc/vent/POWER",
    "cmnd/i3/inside/cnc/light/POWER",
    "cmnd/i3/inside/commons/disco/POWER",
    "cmnd/i3/inside/commons/ceiling-fans/POWER",
    "cmnd/i3/inside/commons/garage-door/lock",
    "cmnd/i3/inside/commons/south-vent/POWER",
    "cmnd/i3/inside/fablab/vent/POWER",
    "cmnd/i3/inside/infrastructure/compressor-valve/POWER",
    "cmnd/i3/inside/large-bathroom/light/POWER",
    "cmnd/i3/inside/large-bathroom/vent/POWER",
    "cmnd/i3/inside/lights/001/POWER",
    "cmnd/i3/inside/lights/002/POWER",
    "cmnd/i3/inside/lights/003/POWER",
    "cmnd/i3/inside/lights/004/POWER",
    "cmnd/i3/inside/lights/005/POWER",
    "cmnd/i3/inside/lights/006/POWER",
    "cmnd/i3/inside/lights/007/POWER",
    "cmnd/i3/inside/lights/008/POWER",
    "cmnd/i3/inside/lights/009/POWER",
    "cmnd/i3/inside/lights/010/POWER",
    "cmnd/i3/inside/lights/011/POWER",
    "cmnd/i3/inside/lights/012/POWER",
    "cmnd/i3/inside/lights/013/POWER",
    "cmnd/i3/inside/lights/014/POWER",
    "cmnd/i3/inside/lights/015/POWER",
    "cmnd/i3/inside/lights/016/POWER",
    "cmnd/i3/inside/lights/017/POWER",
    "cmnd/i3/inside/lights/018/POWER",
    "cmnd/i3/inside/lights/019/POWER",
    "cmnd/i3/inside/lights/020/POWER",
    "cmnd/i3/inside/lights/021/POWER",
    "cmnd/i3/inside/lights/022/POWER",
    "cmnd/i3/inside/lights/023/POWER",
    "cmnd/i3/inside/lights/024/POWER",
    "cmnd/i3/inside/lights/025/POWER",
    "cmnd/i3/inside/lights/026/POWER",
    "cmnd/i3/inside/lights/027/POWER",
    "cmnd/i3/inside/lights/028/POWER",
    "cmnd/i3/inside/lights/029/POWER",
    "cmnd/i3/inside/lights/030/POWER",
    "cmnd/i3/inside/lights/031/POWER",
    "cmnd/i3/inside/lights/032/POWER",
    "cmnd/i3/inside/lights/033/POWER",
    "cmnd/i3/inside/lights/034/POWER",
    "cmnd/i3/inside/lights/035/POWER",
    "cmnd/i3/inside/lights/036/POWER",
    "cmnd/i3/inside/lights/037/POWER",
    "cmnd/i3/inside/lights/038/POWER",
    "cmnd/i3/inside/lights/039/POWER",
    "cmnd/i3/inside/lights/040/POWER",
    "cmnd/i3/inside/infrastructure/air-compressor/POWER",
    "cmnd/i3/inside/laser-zone/ceiling-fan/POWER",
    "cmnd/i3/inside/laser-zone/vent-fan/POWER",
    "cmnd/i3/inside/machine-shop/ceiling-fan/POWER",
    "cmnd/i3/inside/media-lab/lights/POWER",
    "tele/i3/inside/commons/openevse/query",
    "cmnd/i3/inside/commons/paint-box/POWER",
    "cmnd/i3/inside/fablab/chiller/POWER",
    "cmnd/i3/inside/craftroom/light/POWER",
    "cmnd/i3/inside/elab/light/POWER",
    "cmnd/i3/inside/hallway/light/POWER",
    "cmnd/i3/inside/laser-zone/bumblebee/laser/POWER",
    "cmnd/i3/inside/laser-zone/wolverine/laser/POWER",
    "cmnd/i3/inside/small-bathroom/light/POWER"
]

for item in deviceList:
    strip.setPixelColor(item['ledNum'], unknownColor)
strip.show()
time.sleep(wait_ms / 1000.0)


def on_connect(client, userdata, flags, rc):
    # The callback for when the client receives a CONNACK response from the server.
    print("Connected with result code " + str(rc))
    client.publish("tele/i3/inside/commons/map-board/INFO2", "online")

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    for item in deviceList:
        print("subscribing to " + item['topic'])
        client.subscribe(item['topic'])
    for item in pubList:
        client.publish(item, "")


def on_message(client, userdata, msg):
    # The callback for when a PUBLISH message is received from the server.
    for device in deviceList:
        # Match message topic to device, determine state of device
        # Coarse filtering for stat/tele
        if device['topic'][:4] == msg.topic[:4]:
            if device['topic'] == msg.topic:
                # First test for exact payload maches
                if str(device['onState']) == msg.payload:
                    print(device['topic'] + " is ON")
                    device['itemState'] = State.ON
                elif str(device['offState']) == msg.payload:
                    if device['offType'] == State.OFF:
                        print(device['topic'] + " is OFF")
                        device['itemState'] = State.OFF
                    elif device['offType'] == State.DISCONNECTED:
                        print(device['topic'] + " is DISCONNECTED")
                        device['itemState'] = State.DISCONNECTED
                # Then check for partial matches, i.e. look for "Power":"ON" in the middle of telemetry
                # Using this method exclusively breaks for on/off states like locked/unlocked where locked is in unlocked
                elif str(device['onState']) in msg.payload:
                    print(device['topic'] + " is ON")
                    device['itemState'] = State.ON
                elif str(device['offState']) in msg.payload:
                    if device['offType'] == State.OFF:
                        print(device['topic'] + " is OFF")
                        device['itemState'] = State.OFF
                    elif device['offType'] == State.DISCONNECTED:
                        print(device['topic'] + " is DISCONNECTED")
                        device['itemState'] = State.DISCONNECTED
                # Color the device LED
                if device['itemState'] == State.OFF:
                    if device['alwaysOn'] is True:
                        strip.setPixelColor(device['ledNum'], disconnectedColor)
                    elif device['alwaysOn'] is False or device['alwaysOn'] is None:
                        strip.setPixelColor(device['ledNum'], offColor)
                elif device['itemState'] == State.ON:
                    if device['alwaysOn'] is True or device['alwaysOn'] is None:
                        strip.setPixelColor(device['ledNum'], alwaysOnColor)
                    else:
                        strip.setPixelColor(device['ledNum'], onColor)
                elif device['itemState'] == State.DISCONNECTED:
                    strip.setPixelColor(device['ledNum'], disconnectedColor)
                strip.show()
                time.sleep(wait_ms / 1000.0)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("10.13.0.22", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
