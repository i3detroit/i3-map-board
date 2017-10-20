enum lightState{OFF,ON,DISCONNECTED,UNKNOWN};

struct light
{
  int ledNum;		//input pin number
  lightState state;	
  char* mqttTopic;
};
