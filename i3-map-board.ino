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
uint32_t red = pixels.Color(200,0,0);
uint32_t blue = pixels.Color(0,0,200);
uint32_t purple = pixels.Color(200,0,150);
uint32_t green = pixels.Color(0,200,0);
uint32_t yellow = pixels.Color(200,200,0);
uint32_t off = pixels.Color(0,0,0);

int delayVal = 50;

int i = 0;
int j = 0;
int k = 0;

char buf[1024];
const char* host_name = "i3_map_board";
const char* ssid = "i3detroit-wpa";
const char* password = "i3detroit";
const char* mqtt_server = "10.13.0.22";
const int mqtt_port = 1883;

int numLights = ARRAY_SIZE(lights);

void callback(char* topic, byte* payload, unsigned int length, PubSubClient *client) {
  Serial.println("Message arrived [");
  Serial.println(topic);
  Serial.println("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
  uint32_t c;
  for (int j = 0; j < numLights; j++) {
  	Serial.println(topic);
  	Serial.println(lights[j]->mqttTopic);
  	sprintf(buf,"stat%s",lights[j]->mqttTopic);
  	if (strcmp(topic, buf) == 0){
  		Serial.print("yay");
		  if((char)payload[1] == 'N') {
		    lights[j]->state = ON;
		  } else if ((char)payload[1] == 'F') {
		    lights[j]->state = OFF;
		  } else {
		    Serial.println("NOT A THING FUCK");
		    lights[j]->state = DISCONNECTED;
		  }
		}
	}
}

void connectSuccess(PubSubClient* client, char* ip) {
  Serial.println("win");
  //subscribe and shit here
  sprintf(buf, "{\"Hostname\":\"%s\", \"IPaddress\":\"%s\"}", host_name, ip);
  client->publish("tele/i3/inside/commons/map-board/INFO2", buf);
  for (int j = 0; j < numLights; j++) {
  	sprintf(buf,"stat%s",lights[j]->mqttTopic);
		client->subscribe(buf);
		sprintf(buf,"cmnd%s",lights[j]->mqttTopic);
		client->publish(buf, "");
		loop_mqtt();
  }
}

void setup() {
  //start serial connection
  Serial.begin(115200);
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