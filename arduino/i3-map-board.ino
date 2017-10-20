#include <Adafruit_NeoPixel.h>
#include "mqtt-wrapper.h"
#include <items.h>
#include <item_list.h>

#define ARRAY_SIZE(x) (sizeof(x)/sizeof(x[0]))

#define BUTTON_PIN        0  //nodemcu D3
#define PIXEL_PIN					13 //nodemcu D7
#define SWITCH_PIN_A			4  //nodemcu D0
#define SWITCH_PIN_B			12 //nodemcu D6
#define SWITCH_PIN_C			14 //nodemcu D5

#define NUM_PIXELS   60

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUM_PIXELS, PIXEL_PIN, NEO_GRB + NEO_KHZ800);

// define some colors for the neopixels
int brightness = 3; // scale led brightness from 0 to 10
uint32_t ledRed = pixels.Color(25*brightness,0,0);
uint32_t ledBlue = pixels.Color(0,0,25*brightness);
uint32_t ledPurple = pixels.Color(25*brightness,0,18*brightness);
uint32_t ledGreen = pixels.Color(0,25*brightness,0);
uint32_t ledOff = pixels.Color(0,0,0);

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
  //Check if stat/.../POWER update
  if ((char)topic[0] == 's') {
    for (int j = 0; j < numLights; j++) {
      sprintf(buf,"stat%sPOWER",lights[j]->mqttTopic);
      if (strcmp(topic, buf) == 0){
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
      sprintf(buf,"tele%sLWT",lights[j]->mqttTopic);
      if (strcmp(topic, buf) == 0){
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
  Serial.println("connected");
  sprintf(buf, "{\"Hostname\":\"%s\", \"IPaddress\":\"%s\"}", host_name, ip);
  client->publish("tele/i3/inside/commons/map-board/INFO2", buf);
  loop_mqtt();

  client->subscribe("stat/i3/commons/lights/+/POWER");
  loop_mqtt();
  client->subscribe("tele/i3/commons/lights/+/LWT");
  loop_mqtt();
  client->publish("cmnd/i3/commons/lights/all/POWER", " ");
  loop_mqtt();
  Serial.println("lights loaded");

  client->subscribe("stat/i3/inside/commons/east-ceiling-fans/POWER");
  loop_mqtt();
  client->subscribe("tele/i3/inside/commons/east-ceiling-fans/LWT");
  loop_mqtt();
  client->publish("cmnd/i3/inside/commons/east-ceiling-fans/POWER", " ");
  loop_mqtt();
  Serial.println("east fans loaded");

  // client->subscribe("stat/i3/machineShop/fans/ceilingFan/POWER");
  // loop_mqtt();
  // client->subscribe("tele/i3/machineShop/fans/ceilingFan/LWT");
  // loop_mqtt();
  // client->publish("cmnd/i3/machineShop/fans/ceilingFan/POWER", " ");
  // loop_mqtt();
  // Serial.println("machine shop fan loaded");

  // client->subscribe("stat/i3/laserZone/ceilingFan/POWER");
  // loop_mqtt();
  // client->subscribe("tele/i3/laserZone/ceilingFan/LWT");
  // loop_mqtt();
  // client->publish("cmnd/i3/laserZone/ceilingFan/POWER", " ");
  // loop_mqtt();
  // Serial.println("laser ceiling fan loaded");

  // client->subscribe("stat/i3/laserZone/ventFan/POWER");
  // loop_mqtt();
  // client->subscribe("tele/i3/laserZone/ventFan/LWT");
  // loop_mqtt();
  // client->publish("cmnd/i3/laserZone/ventFan/POWER", " ");
  // loop_mqtt();
  // Serial.println("laser vent loaded");

  // client->subscribe("stat/i3/inside/fablab/vent/POWER");
  // loop_mqtt();
  // client->subscribe("tele/i3/inside/fablab/vent/LWT");
  // loop_mqtt();
  // client->publish("cmnd/i3/inside/fablab/vent/POWER", " ");
  // loop_mqtt();
  // Serial.println("fab lab vent loaded");

  // client->subscribe("stat/i3/inside/office-bathroom/light/POWER");
  // loop_mqtt();
  // client->subscribe("tele/i3/inside/office-bathroom/light/LWT");
  // loop_mqtt();
  // client->publish("cmnd/i3/inside/office-bathroom/light/POWER", " ");
  // loop_mqtt();
  // Serial.println("Bathroom light loaded");

  // client->subscribe("stat/i3/inside/commons/bathroom-vent-fan/POWER");
  // loop_mqtt();
  // client->subscribe("tele/i3/inside/commons/bathroom-vent-fan/LWT");
  // loop_mqtt();
  // client->publish("cmnd/i3/inside/commons/bathroom-vent-fan/POWER", " ");
  // loop_mqtt();
  // Serial.println("Bathroom fan loaded");
}


void setup() {
  //start serial connection
  Serial.begin(115200);
  setup_mqtt(connectedLoop, callback, connectSuccess, ssid, password, mqtt_server, mqtt_port, host_name);
  pixels.begin();
  for (int j=0; j < NUM_PIXELS; j++) {
    pixels.setPixelColor(j,ledPurple);
  }
  pixels.show();
  delay(2000);
  for (int j=0; j < NUM_PIXELS; j++) {
     pixels.setPixelColor(j,ledOff);
  }
  // Map key
  pixels.setPixelColor(1,ledGreen);
  pixels.setPixelColor(2,ledRed);
  pixels.setPixelColor(3,ledBlue);
  pixels.setPixelColor(4,ledPurple);
  Serial.print("Setup complete");
}

void connectedLoop(PubSubClient* client) {
  for (int j = 0; j < numLights; j++) {
    setLED(*lights[j]);
  }
  pixels.show();
  delay(delayVal);
  //Serial.print("looped");
}

void loop() {
  loop_mqtt();
}

void setLED(light device) {
  if (device.state == ON) {
    pixels.setPixelColor(device.ledNum,ledGreen);
  } else if (device.state == OFF) {
    pixels.setPixelColor(device.ledNum,ledRed);
  } else if (device.state == DISCONNECTED) {
    pixels.setPixelColor(device.ledNum,ledBlue);
  } else if (device.state == UNKNOWN) {
    pixels.setPixelColor(device.ledNum,ledPurple);
  }
}