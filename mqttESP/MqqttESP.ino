#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// Here we declare the variables;
float var;
float tempf=40;
char temp[8];
const char* ssid = "red"; //put here the ssid of your wifi
const char* password = "12345678"; //put here the pasword of your wifi
const char* mqtt_server = "192.168.43.119"; //put here the raspberry ip (the mosquitto server )
char ordrechar;
int ordre;
WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;
int heater = 4; //the pin output of the heater
int mixer = 2; //the pin output of the mixer

void setup() {
  pinMode(heater,OUTPUT);     
  pinMode(mixer, OUTPUT);
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  
}

void setup_wifi() {

  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) 
    {
    Serial.print((char)payload[i]);//here we will print the order recieved in the serial port
    }
  Serial.println();

  // Here we will  activate or deactivate the outputs depending the message recived 
  if ((char)payload[0] == '1')
    {
    digitalWrite(heater, HIGH);
    Serial.print("the heater is now on");
    }

    if ((char)payload[0] == '2') 
    {
    digitalWrite(heater, LOW);
    Serial.print("the heater is now off");
    }

    if ((char)payload[0] == '3')
    {
    digitalWrite(mixer, HIGH);
    Serial.print("the mixer is now on");
    }

    if ((char)payload[0] == '4') 
    {
    digitalWrite(mixer, LOW);
    Serial.print("the mixer is now off");
    } 
}

void reconnect() {
  // Loop until we're reconnected
  WiFi.mode(WIFI_STA);
  while (!client.connected()) {
  Serial.print("Attempting MQTT connection...");
  // Attempt to connect
  if (client.connect("ESP8266Client")) 
  {
      Serial.println("connected");
      client.subscribe("relesarduino"); // Put here the relays topic  
   } else 
   {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
   }
  }
}

void loop() 
{
// this part will simulate the temperature sensor
  var=random(-5, 5);
  tempf= abs(tempf + var);
  dtostrf(tempf,6, 2, temp);
  delay(1000);
//Conection loop
  if (!client.connected()) 
     {
      reconnect();
      delay(1000);
     }
  client.loop();
 
   
  //here we send the temperature
  client.publish("sensortemp", temp); // Put here the sensor topic
  


  
  
 }
