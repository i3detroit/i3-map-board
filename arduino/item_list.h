//struct, type, name,	led, initial state,	topic
struct light light005 = {5,UNKNOWN,"/i3/commons/lights/scuzzLights005/"};
struct light light001 = {6,UNKNOWN,"/i3/commons/lights/scuzzLights001/"};
struct light light028 = {7,UNKNOWN,"/i3/commons/lights/scuzzLights028/"};
struct light light002 = {8,UNKNOWN,"/i3/commons/lights/scuzzLights002/"};
struct light light003 = {9,UNKNOWN,"/i3/commons/lights/scuzzLights003/"};
struct light light004 = {10,UNKNOWN,"/i3/commons/lights/scuzzLights004/"};
struct light light029 = {11,UNKNOWN,"/i3/commons/lights/scuzzLights029/"};
struct light light030 = {12,UNKNOWN,"/i3/commons/lights/scuzzLights030/"};
struct light light032 = {13,UNKNOWN,"/i3/commons/lights/scuzzLights032/"};
struct light light031 = {14,UNKNOWN,"/i3/commons/lights/scuzzLights031/"};
struct light fan003   = {15,UNKNOWN,"/i3/machineShop/fans/ceilingFan/"}; // machine shop fan
struct light light009 = {16,UNKNOWN,"/i3/commons/lights/scuzzLights009/"};
struct light fan001   = {17,UNKNOWN,"/i3/inside/commons/east-ceiling-fans/"}; // commons fans
struct light light008 = {18,UNKNOWN,"/i3/commons/lights/scuzzLights008/"};
struct light light007 = {19,UNKNOWN,"/i3/commons/lights/scuzzLights007/"};
struct light light006 = {20,UNKNOWN,"/i3/commons/lights/scuzzLights006/"};
struct light fan002   = {21,UNKNOWN,"/i3/inside/commons/east-ceiling-fans/"}; // commons fans
struct light snapple  = {22,UNKNOWN,"/i3/commons/lights/snappleVending/"};
struct light light010 = {23,UNKNOWN,"/i3/commons/lights/scuzzLights010/"};
struct light light011 = {24,UNKNOWN,"/i3/commons/lights/scuzzLights011/"};
struct light light012 = {25,UNKNOWN,"/i3/commons/lights/scuzzLights012/"};
struct light light013 = {26,UNKNOWN,"/i3/commons/lights/scuzzLights013/"};
struct light light014 = {27,UNKNOWN,"/i3/commons/lights/scuzzLights014/"};
struct light light035 = {28,UNKNOWN,"/i3/commons/lights/scuzzLights035/"};
struct light light034 = {29,UNKNOWN,"/i3/commons/lights/scuzzLights034/"};
struct light light033 = {30,UNKNOWN,"/i3/commons/lights/scuzzLights033/"};
struct light light019 = {31,UNKNOWN,"/i3/commons/lights/scuzzLights019/"};
struct light light025 = {32,UNKNOWN,"/i3/commons/lights/scuzzLights025/"};
struct light light026 = {33,UNKNOWN,"/i3/commons/lights/scuzzLights026/"};
struct light light018 = {34,UNKNOWN,"/i3/commons/lights/scuzzLights018/"};
struct light light017 = {35,UNKNOWN,"/i3/commons/lights/scuzzLights017/"};
struct light light024 = {36,UNKNOWN,"/i3/commons/lights/scuzzLights024/"};
struct light light023 = {37,UNKNOWN,"/i3/commons/lights/scuzzLights023/"};
struct light light016 = {38,UNKNOWN,"/i3/commons/lights/scuzzLights016/"};
struct light fan006   = {39,UNKNOWN,"/i3/inside/fablab/vent/"}; // fab lab exhaust
struct light light022 = {40,UNKNOWN,"/i3/commons/lights/scuzzLights022/"};
struct light light036 = {41,UNKNOWN,"/i3/commons/lights/scuzzLights036/"};
struct light light021 = {42,UNKNOWN,"/i3/commons/lights/scuzzLights021/"};
struct light fan004   = {43,UNKNOWN,"/i3/laserZone/ceilingFan/"}; // laser zone ceiling fan
struct light light037 = {44,UNKNOWN,"/i3/commons/lights/scuzzLights037/"};
struct light fan005   = {45,UNKNOWN,"/i3/laserZone/ventFan/"}; // laser zone exhaust
struct light light015 = {46,UNKNOWN,"/i3/commons/lights/scuzzLights015/"};
struct light light020 = {47,UNKNOWN,"/i3/commons/lights/scuzzLights020/"};
struct light light027 = {48,UNKNOWN,"/i3/commons/lights/scuzzLights027/"};
struct light balight1 = {49,UNKNOWN,"/i3/inside/office-bathroom/light/"};
struct light bafan01  = {50,UNKNOWN,"/i3/inside/commons/bathroom-vent-fan/"};

struct light *lights[] = {&light001, &light002, &light003, &light004, &light005, 
	&light006, &light007, &light008, &light009, &light010, &light011, &light012, 
	&light013, &light014, &light015, &light016, &light017, &light018, &light019, 
	&light020, &light021, &light022, &light023, &light024, &light025, &light026, 
	&light027, &light028, &light029, &light030, &light031, &light032, &light033, 
	&light034, &light035, &light036, &light037, &fan001, &fan002, &fan003,
	&fan004, &fan005, &fan006, &snapple, &balight1, &bafan01};