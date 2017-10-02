#include <Adafruit_NeoPixel.h>
#include "mqtt-wrapper.h"
#include <items.h>
#include <item_list.h>

#define ARRAY_SIZE(x) (sizeof(x)/sizeof(x[0]))

#define PIXEL_PIN					13 //nodemcu D7
#define SWITCH_PIN_A			4  //nodemcu D0
#define SWITCH_PIN_B			12 //nodemcu D6
#define SWITCH_PIN_C			14 //nodemcu D5

#define NUM_PIXELS   50

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUM_PIXELS, PIXEL_PIN, NEO_GRB + NEO_KHZ800);

// define some colors for the neopixels
uint32_t red = pixels.Color(15,0,0);
uint32_t blue = pixels.Color(0,0,15);
uint32_t purple = pixels.Color(15,0,10);
uint32_t green = pixels.Color(0,15,0);
uint32_t yellow = pixels.Color(15,15,0);
uint32_t off = pixels.Color(0,0,0);

int delayVal = 50;

int i = 0;
int j = 0;
int k = 0;

char bufA[1024];
char bufB[1024];
const char* host_name = "i3_map_board";
const char* ssid = "i3detroit-wpa";
const char* password = "i3detroit";
const char* mqtt_server = "10.13.0.22";
const int mqtt_port = 1883;

int numLights = ARRAY_SIZE(lights);

void callback(char* topic, byte* payload, unsigned int length, PubSubClient *client) {
  //Check if stat/.../POWER update
  if ((char)topic[0] == 's') {
    for (int j = 0; j < numLights; j++) {
      sprintf(bufA,"stat%sPOWER",lights[j]->mqttTopic);
      if (strcmp(topic, bufA) == 0){
        if((char)payload[1] == 'N') {
          lights[j]->state = ON;
        } else if ((char)payload[1] == 'F') {
          lights[j]->state = OFF;
        } else {
          lights[j]->state = UNKNOWN;
        }
      }
    }
  }
  //Check if tele/.../LWT update
  else if ((char)topic[0] == 't') {
    for (int j = 0; j < numLights; j++) {
      sprintf(bufB,"tele%sLWT",lights[j]->mqttTopic);
      if (strcmp(topic, bufB) == 0){
        if((char)payload[1] == 'n') {
          lights[j]->state = ON;
        } else if ((char)payload[1] == 'f') {
          lights[j]->state = DISCONNECTED;
        } else {
          lights[j]->state = UNKNOWN;
        }
      }
    }
  }
}

void connectSuccess(PubSubClient* client, char* ip) {
  //Serial.println("win");
  //subscribe and shit here
  sprintf(bufA, "{\"Hostname\":\"%s\", \"IPaddress\":\"%s\"}", host_name, ip);
  client->publish("tele/i3/inside/commons/map-board/INFO2", bufA);
  client->subscribe("stat/i3/commons/lights/+/POWER");
  client->subscribe("tele/i3/commons/lights/+/LWT");
  client->publish("cmnd/i3/commons/lights/all/POWER", " ");
}

void setup() {
  //start serial connection
  //Serial.begin(115200);
  setup_mqtt(connectedLoop, callback, connectSuccess, ssid, password, mqtt_server, mqtt_port, host_name);
  pixels.begin(); // This initializes the NeoPixel library.
  for (int j=0; j < NUM_PIXELS; j++) {
    pixels.setPixelColor(j,purple);
  }
  pixels.show();
  delay(2000);
  for (int j=0; j < NUM_PIXELS; j++) {
     pixels.setPixelColor(j,off);
  }
  pixels.setPixelColor(1,green);
  pixels.setPixelColor(2,red);
  pixels.setPixelColor(3,blue);
  pixels.setPixelColor(4,purple);
  pixels.show();
}

void connectedLoop(PubSubClient* client) {

}

void loop() {
	loop_mqtt();
	for (int j = 0; j < numLights; j++) {
		if (lights[j]->state == ON) {
			ledOn(*lights[j]);
		}
		else if (lights[j]->state == OFF) {
			ledOff(*lights[j]);
		}
		else if (lights[j]->state == DISCONNECTED) {
			ledDisconnected(*lights[j]);
		}
		else if (lights[j]->state == UNKNOWN) {
			ledUnknown(*lights[j]);
		}
	}
  pixels.show();
  delay(delayVal);
}

void ledOn(light device) {
	pixels.setPixelColor(device.ledNum,green);
}
void ledOff(light device) {
	pixels.setPixelColor(device.ledNum,red);
}
void ledDisconnected(light device) {
	pixels.setPixelColor(device.ledNum,blue);
}
void ledUnknown(light device) {
	pixels.setPixelColor(device.ledNum,purple);
}