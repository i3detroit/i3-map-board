# i3-map-board
Display for device statuses such as lights, fans, etc.

https://www.i3detroit.org/wiki/MQTT_Space_Map

Via MQTT, subscribes to status and telemetry messages from light fixtures, door sensors, exhaust fans, disco balls, etc.  and then outputs device states to LEDs

`map.py` is designed to run on a Raspberry Pi Zero W with neopixels/WS281X on pin 18.
`leds.yaml` contains the list of LEDs and which MQTT topics/payloads correspond to which light states.

<img src="https://www.i3detroit.org/wi/images/thumb/d/d5/IoT_map.jpg/768px-IoT_map.jpg" alt="The map" width="400">
