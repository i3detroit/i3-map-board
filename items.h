enum lightState{OFF,ON,DISCONNECTED,UNKNOWN};

struct light
{
  int ledNum;		//input pin number
  lightState state;		//State of the switch - 0 off, 1 on
  char* mqttTopic;
};