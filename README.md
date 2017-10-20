# i3-map-board
Display board for device statuses such as lights, fans, etc.

Initially written for arduino to run on an esp8266, then rewritten in python to run on a raspberry pi zero w. The arduino version does not function fully, due to problems subscribing to too many MQTT topics.

Via MQTT, subscribes to all status (POWER) and telemetry (LWT) messages from lighting, ceiling fans, exhaust fans, etc.  and then outputs states to ws2812 LEDs

items.h includes the definitions of device types being tracked
items_list.h includes declarations for each individual device to store indivudual device states, output LED numbers, MQTT topic, etc.
These were merged with the main program in the python version.
