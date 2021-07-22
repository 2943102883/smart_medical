#include <UIPEthernet.h>
#include <PubSubClient.h>
#include <DHTxx.h>
#define CLIENT_ID       "720373994"
#define USERNAME        "428390"
#define PASSWORD        "ar123456"
#define PUB_TOPIC       "temperature"
#define SUB_TOPIC       "feng"
#define PUBLISH_DELAY   5000
DHTXX io_HTS1 = DHTXX (8, 11);
uint8_t mac[6] = {0x00,0x01,0x02,0x03,0x04,0x05};
EthernetClient ethClient;
PubSubClient mqttClient;
long previousMillis;
//dc
int Motor1 = 7;
int Motor2 = 6;
int Motor3 = 5;
int Motor4 = 4;
void setup() {
// setup serial communication
Serial.begin(9600);
while(!Serial) {};
Serial.println(F("OneNet"));
Serial.println();  
// setup ethernet communication using DHCP
if(Ethernet.begin(mac) == 0) {
    Serial.println(F("Unable to configure Ethernet using DHCP"));
    for(;;);
}
Serial.println(F("Ethernet configured via DHCP"));
Serial.print("IP address: ");
Serial.println(Ethernet.localIP());
Serial.println();
// setup mqtt client
mqttClient.setClient(ethClient);
mqttClient.setServer("183.230.40.39", 6002);
mqttClient.setCallback(mqttCallback);
Serial.println(F("MQTT client configured"));
// setup DHT sensor
io_HTS1.begin();
mqttConnect();
Serial.println();
Serial.println(F("Ready!"));
previousMillis = millis();
//dc
pinMode(Motor1, OUTPUT);
pinMode(Motor2, OUTPUT);
pinMode(Motor3, OUTPUT);
pinMode(Motor4, OUTPUT);   
digitalWrite(Motor1, HIGH);
digitalWrite(Motor2, HIGH);
digitalWrite(Motor3, HIGH);
digitalWrite(Motor4, HIGH);
}

void loop() {

  // it's time to send new data?
if(millis() - previousMillis > PUBLISH_DELAY) {
    sendData();
    previousMillis = millis();
}

mqttClient.loop();
}

void mqttConnect() {

while(!mqttClient.connected()) {
    
    if(mqttClient.connect(CLIENT_ID, USERNAME, PASSWORD)) {

    Serial.println(F("MQTT client connected"));
    mqttClient.subscribe(SUB_TOPIC);
    Serial.println(F("Topic subscribed"));
    } else {
    Serial.println(F("Unable to connect, retry in 5 seconds"));
    delay(5000);
    }
}
}

void mqttCallback(char* topic, byte* payload, unsigned int length) {

// Serial.println((const char*)payload);
if(strncmp((const char*)payload, "1", 1)==0) {
    Serial.println("ON message received, turning relay ON");
    digitalWrite(Motor2, LOW);
    digitalWrite(Motor1, HIGH); 
    Serial.println("First Motor is moving in Clockwise Direction.");
    
} else {
    Serial.println("OFF message received, turning relay OFF");
    digitalWrite(Motor1, LOW);
    digitalWrite(Motor2,  LOW); 
    Serial.println("First Motor is Stopped");
}
}

void sendData() {

char msgBuffer[50]; 
float var_Humidity=io_HTS1.readHumidity();
float var_tCelsius=io_HTS1.readTemperature(0);
float var_tFarhenheit=io_HTS1.readTemperature(1);
Serial.println(var_Humidity);
Serial.println(var_tCelsius);
Serial.println(var_tFarhenheit);
if(!mqttClient.connected()) mqttConnect();
char msg[50];
char tmp[28];
char d[3];
//publish
mqttClient.publish("w", dtostrf(var_tCelsius, 0, 0, msgBuffer)); 
//save db
snprintf(tmp,sizeof(msgBuffer),"{\"temperature\":%s}",msgBuffer);
Serial.println(tmp);
uint16_t streamLen= strlen(tmp);
d[0]='\x03';
d[1] = (streamLen >> 8);
d[2] = (streamLen & 0xFF);
snprintf(msg,sizeof(msg),"%c%c%c%s",d[0],d[1],d[2],tmp);
mqttClient.publish("$dp", (uint8_t*)msg,streamLen+3,false);

//publish
mqttClient.publish("s", dtostrf(var_Humidity, 0, 0, msgBuffer));
//save db
snprintf(tmp,sizeof(msgBuffer),"{\"humidity\":%s}",msgBuffer);
Serial.println(tmp);
uint16_t streamLen2= strlen(tmp);
d[0]='\x03';
d[1] = (streamLen2 >> 8);
d[2] = (streamLen2 & 0xFF);
snprintf(msg,sizeof(msg),"%c%c%c%s",d[0],d[1],d[2],tmp);
mqttClient.publish("$dp", (uint8_t*)msg,streamLen2+3,false);
}