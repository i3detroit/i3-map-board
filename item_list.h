//struct, type, name,	led, initial state,	topic
struct light light005 = {4,UNKNOWN,"/i3/commons/lights/scuzzLights005/"};
struct light light001 = {5,UNKNOWN,"/i3/commons/lights/scuzzLights001/"};
struct light light028 = {6,UNKNOWN,"/i3/commons/lights/scuzzLights028/"};
struct light light002 = {7,UNKNOWN,"/i3/commons/lights/scuzzLights002/"};
struct light light003 = {8,UNKNOWN,"/i3/commons/lights/scuzzLights003/"};
struct light light004 = {9,UNKNOWN,"/i3/commons/lights/scuzzLights004/"};
struct light light029 = {10,UNKNOWN,"/i3/commons/lights/scuzzLights029/"};
struct light light030 = {11,UNKNOWN,"/i3/commons/lights/scuzzLights030/"};
struct light light032 = {12,UNKNOWN,"/i3/commons/lights/scuzzLights032/"};
struct light light031 = {13,UNKNOWN,"/i3/commons/lights/scuzzLights031/"};
struct light fan003 = {14,UNKNOWN,"/i3/machineShop/fans/ceilingFan/"}; // machine shop fan
struct light light009 = {15,UNKNOWN,"/i3/commons/lights/scuzzLights009/"};
struct light fan001 = {16,UNKNOWN,"/i3/inside/commons/east-ceiling-fans/"}; // commons fans
struct light light008 = {17,UNKNOWN,"/i3/commons/lights/scuzzLights008/"};
struct light light007 = {18,UNKNOWN,"/i3/commons/lights/scuzzLights007/"};
struct light light006 = {19,UNKNOWN,"/i3/commons/lights/scuzzLights006/"};
struct light fan002 = {20,UNKNOWN,"/i3/inside/commons/east-ceiling-fans/"}; // commons fans
struct light snapple = {21,UNKNOWN,"/i3/commons/lights/snappleVending/"};
struct light light010 = {22,UNKNOWN,"/i3/commons/lights/scuzzLights010/"};
struct light light011 = {23,UNKNOWN,"/i3/commons/lights/scuzzLights011/"};
struct light light012 = {24,UNKNOWN,"/i3/commons/lights/scuzzLights012/"};
struct light light013 = {25,UNKNOWN,"/i3/commons/lights/scuzzLights013/"};
struct light light014 = {26,UNKNOWN,"/i3/commons/lights/scuzzLights014/"};
struct light light035 = {27,UNKNOWN,"/i3/commons/lights/scuzzLights035/"};
struct light light034 = {28,UNKNOWN,"/i3/commons/lights/scuzzLights034/"};
struct light light033 = {29,UNKNOWN,"/i3/commons/lights/scuzzLights033/"};
struct light light019 = {30,UNKNOWN,"/i3/commons/lights/scuzzLights019/"};
struct light light025 = {31,UNKNOWN,"/i3/commons/lights/scuzzLights025/"};
struct light light026 = {32,UNKNOWN,"/i3/commons/lights/scuzzLights026/"};
struct light light018 = {33,UNKNOWN,"/i3/commons/lights/scuzzLights018/"};
struct light light017 = {34,UNKNOWN,"/i3/commons/lights/scuzzLights017/"};
struct light light024 = {35,UNKNOWN,"/i3/commons/lights/scuzzLights024/"};
struct light light023 = {36,UNKNOWN,"/i3/commons/lights/scuzzLights023/"};
struct light light016 = {37,UNKNOWN,"/i3/commons/lights/scuzzLights016/"};
struct light fan006 = {38,UNKNOWN,"/i3/inside/fablab/vent/"}; // fab lab exhaust
struct light light022 = {39,UNKNOWN,"/i3/commons/lights/scuzzLights022/"};
struct light light036 = {40,UNKNOWN,"/i3/commons/lights/scuzzLights036/"};
struct light light021 = {41,UNKNOWN,"/i3/commons/lights/scuzzLights021/"};
struct light fan004 = 	{42,UNKNOWN,"/i3/laserZone/ceilingFan/"}; // laser zone ceiling fan
struct light light037 = {43,UNKNOWN,"/i3/commons/lights/scuzzLights037/"};
struct light fan005 = {44,UNKNOWN,"/i3/laserZone/ventFan/"}; // laser zone exhaust
struct light light015 = {45,UNKNOWN,"/i3/commons/lights/scuzzLights015/"};
struct light light020 = {46,UNKNOWN,"/i3/commons/lights/scuzzLights020/"};
struct light light027 = {47,UNKNOWN,"/i3/commons/lights/scuzzLights027/"};
struct light bathlight001 = {48,UNKNOWN,"/i3/inside/office-bathroom/light/"};
struct light bathfan001 = {49,UNKNOWN,"/i3/inside/commons/bathroom-vent-fan/"};

struct light *lights[] = {&light001, &light002, &light003, &light004, &light005, 
	&light006, &light007, &light008, &light009, &light010, &light011, &light012, 
	&light013, &light014, &light015, &light016, &light017, &light018, &light019, 
	&light020, &light021, &light022, &light023, &light024, &light025, &light026, 
	&light027, &light028, &light029, &light030, &light031, &light032, &light033, 
	&light034, &light035, &light036, &light037, &fan001, &fan002, &fan003,
	&fan004, &fan005, &fan006, &snapple, &bathlight001, &bathfan001};