#!/usr/bin/env python3
# MQTT controlled LED board
# Each LED represents one device which can have multiple MQTT topics
# that report it's state (i.e. regular telemetry, reporting received
# commands, LWT)
# 2019 Mike Fink
# MIT License

import yaml
import re
import paho.mqtt.client as mqtt
import time
import neopixel
import board

mqtt_host = '10.13.0.22'
mqtt_port = 1883

led_file = 'leds.yaml'

# LED strip configuration:
LED_COUNT = 100       # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 5           # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True inverts the signal
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
#LED_STRIP = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

wait_ms = 50
strip = neopixel.NeoPixel(board.D18, LED_COUNT)
# strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA,
#                           LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL,
#                           LED_STRIP)
# strip.begin()

brightness = 4
disconnectedColor = (25 * brightness, 0, 0)           # red
alwaysOnColor = (25 * brightness, 10 * brightness, 0) # amber
unknownColor = (25 * brightness, 0, 18 * brightness)  # purple
onColor = (0, 25 * brightness, 0)                     # green
offColor = (0, 0, 25 * brightness)                    # blue
ledDarkColor = (0,0,0)                                # off

with open(led_file, 'r') as f:
    leds = yaml.safe_load(f)

# Replace led_state strings with color objects
for led in leds:
    for t in led['topics']:
        for p in t['payloads']:
            print(p)
            if p['led_state'] == 'on_good':
                p['led_state'] = alwaysOnColor
            elif p['led_state'] == 'on_bad':
                p['led_state'] = onColor
            elif p['led_state'] == 'off_good':
                p['led_state'] = offColor
            elif p['led_state'] == 'off_bad':
                p['led_state'] = disconnectedColor
            elif p['led_state'] == 'disconnected':
                p['led_state'] = disconnectedColor

# Map legend
strip[1] = unknownColor
strip[2] = onColor
strip[3] = alwaysOnColor
strip[4] = offColor
strip[5] = disconnectedColor

# Initialize all LEDs to unknown
for led in leds:
    for l in led['leds']:
        strip[l] = unknownColor
strip.show()
time.sleep(wait_ms / 1000.0)

def on_connect(client, userdata, flags, rc):
    ''' The callback for when the client connects to the server. '''
    print("Connected with result code " + str(rc))
    client.publish("tele/i3/inside/commons/map-board/INFO2", "Online")

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    for led in leds:
        for t in led['topics']:
            print('subscribing to ' + t['topic'])
            client.subscribe(t['topic'])
        client.publish(led['query_command'], "")

def check_message(msg):
    ''' 
    Check which LED the message is for.
    Return the LED number and the color associated with the message payload.
    '''
    #print('checking message {topic}'.format(topic=msg.topic))
    for l in leds:
        for t in l['topics']:
            if t['topic'] == msg.topic:
                #print('Matched {topic} {payload}'.format(topic=msg.topic, payload=msg.payload))
                for p in t['payloads']:
                    # Some expected payloads are variable (i.e. tasmota 
                    # telemetry json) so some are given as regex patterns
                    pattern = re.compile(p['payload'])
                    if re.fullmatch(pattern, msg.payload.decode('UTF-8')) is not None:
                        print(msg.topic, msg.payload.decode('UTF-8'), p['led_state'])
                        # print('matched {pattern}.'.format(pattern=pattern))
                        return l['leds'], p['led_state']

def on_message(client, userdata, msg):
    ''' Get led number and color and set it. '''
    led_nums, led_color = check_message(msg)
    if led_nums is not None and led_color is not None:
        for led_num in led_nums:
            strip[led_num] = led_color
        blue =  led_color & 255
        green = (led_color >> 8) & 255
        red =   (led_color >> 16) & 255
        print('{top} set to {msg.payload} ({red}, {green}, {blue})'.format(top=msg.topic, red=red, green=green, blue=blue))
        strip.show()
        time.sleep(wait_ms / 1000.0)

# Create the mqtt client and connect to the server
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_host, mqtt_port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
client.loop_forever()

### Testing
# with open('test_data.log', 'r') as f:
#     raw_data = f.readlines()
# # raw_data = ['tele/i3/inside/lights/005/STATE {"Time":"2019-08-29T11:23:09","Uptime":"12T01:01:31","Vcc":3.183,"SleepMode":"Dynamic","Sleep":50,"LoadAvg":19,"POWER":"ON","Wifi":{"AP":1,"SSId":"i3detroit-iot","BSSId":"02:9F:C2:24:30:D7","Channel":9,"RSSI":86,"LinkCount":1,"Downtime":"0T00:00:08"}}']
# test_data = []
# for l in raw_data:
#     a = l.split(' ')
#     test_data.append({'topic': a[0], 'payload': a[1]})
# # print(test_data[25])

