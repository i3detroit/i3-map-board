# i3-map-board
Display board for device statuses such as lights, fans, etc.

Via MQTT, subscribes to all light status (POWER) and telemetry (LWT) messages and outputs states to LEDs

items.h includes the definitions of device types being tracked (currently only lights).
items_list.h includes declarations for each individual device struct to store indivudual device states, output LED numbers, MQTT topic, etc.
