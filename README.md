# i3-map-board
Display for device statuses such as lights, fans, etc.

Via MQTT, subscribes to status and telemetry messages from light fixtures, door sensors, exhaust fans, disco balls, etc.  and then outputs device states to LEDs

i3_map_board.py is designed to run on a Raspberry Pi Zero W with neopixels/WS281X on pin 18.
items_list.ods is a spreadsheet to clearly store and generate the MQTT items list dictionary. Add items and then copy the whole thing back into the pyhton script.

Initially written for arduino to run on an esp8266, then rewritten in python for a pi. The arduino version does not fully function, due to problems subscribing to too many MQTT topics.

<img src="https://www.i3detroit.org/wi/images/thumb/d/d5/IoT_map.jpg/768px-IoT_map.jpg" alt="The map" width="400">
