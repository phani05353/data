#include <WiFi.h>
extern "C" {
  #include "freertos/FreeRTOS.h"
  #include "freertos/timers.h"
}
#include <AsyncMqttClient.h>
#include <Wire.h>
#include <OneWire.h>
#include <DallasTemperature.h>
 
//replace with your network credentials
#define WIFI_SSID "**********"
#define WIFI_PASSWORD "************"

// Raspberry Pi Mosquitto MQTT Broker
#define MQTT_HOST IPAddress(*,*,*,*)
#define MQTT_PORT 1883

//MQTT Topics
#define MQTT_PUB_TEMP_C "esp32/ds18b20/temperatureC"
#define MQTT_PUB_TEMP_F  "esp32/ds18b20/temperatureF"

const int SensorDataPin = 4;   
  
OneWire oneWire(SensorDataPin);
DallasTemperature sensors(&oneWire);

float temperature_Celsius;
float temperature_Fahrenheit;

AsyncMqttClient mqttClient;
TimerHandle_t mqttReconnectTimer;
TimerHandle_t wifiReconnectTimer;

unsigned long previousMillis = 0;   
const long interval = 5000;        

void connectToWifi() {
  Serial.println("Connecting to Wi-Fi...");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
}

void connectToMqtt() {
  Serial.println("Connecting to MQTT...");
  mqttClient.connect();
}

void WiFiEvent(WiFiEvent_t event) {
  Serial.printf("[WiFi-event] event: %d\n", event);
  switch(event) {
    case SYSTEM_EVENT_STA_GOT_IP:
      Serial.println("WiFi connected");
      Serial.println("IP address: ");
      Serial.println(WiFi.localIP());
      connectToMqtt();
      break;
    case SYSTEM_EVENT_STA_DISCONNECTED:
      Serial.println("WiFi lost connection");
      xTimerStop(mqttReconnectTimer, 0); 
      xTimerStart(wifiReconnectTimer, 0);
      break;
  }
}

void onMqttConnect(bool sessionPresent) {
  Serial.println("Connected to MQTT.");
  Serial.print("Session present: ");
  Serial.println(sessionPresent);
}

void onMqttDisconnect(AsyncMqttClientDisconnectReason reason) {
  Serial.println("Disconnected from MQTT.");
  if (WiFi.isConnected()) {
    xTimerStart(mqttReconnectTimer, 0);
  }
}

void onMqttPublish(uint16_t packetId) {
  Serial.print("Publish acknowledged.");
  Serial.print("  packetId: ");
  Serial.println(packetId);
}

void setup() {
  Serial.begin(115200);
  Serial.println();
  
  sensors.begin();
  
  mqttReconnectTimer = xTimerCreate("mqttTimer", pdMS_TO_TICKS(2000), pdFALSE, (void*)0, reinterpret_cast<TimerCallbackFunction_t>(connectToMqtt));
  wifiReconnectTimer = xTimerCreate("wifiTimer", pdMS_TO_TICKS(2000), pdFALSE, (void*)0, reinterpret_cast<TimerCallbackFunction_t>(connectToWifi));

  WiFi.onEvent(WiFiEvent);

  mqttClient.onConnect(onMqttConnect);
  mqttClient.onDisconnect(onMqttDisconnect);
  mqttClient.onPublish(onMqttPublish);
  mqttClient.setServer(MQTT_HOST, MQTT_PORT);
  connectToWifi();
}

void loop() {
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
     sensors.requestTemperatures(); 
     temperature_Celsius = sensors.getTempCByIndex(0);
     temperature_Fahrenheit = sensors.getTempFByIndex(0);
    
    
    // Publish an MQTT message on topic esp32/ds18b20/temperatureC
    uint16_t packetIdPub1 = mqttClient.publish(MQTT_PUB_TEMP_C, 1, true, String(temperature_Celsius).c_str());                            
    Serial.printf("Publishing on topic %s at QoS 1, packetId: %i", MQTT_PUB_TEMP_C, packetIdPub1);
    Serial.printf("Message: %.2f \n", temperature_Celsius);

    // Publish an MQTT message on topic esp32/ds18b20/temperatureF
    uint16_t packetIdPub2 = mqttClient.publish(MQTT_PUB_TEMP_F, 1, true, String(temperature_Fahrenheit).c_str());                            
    Serial.printf("Publishing on topic %s at QoS 1, packetId %i: ", MQTT_PUB_TEMP_F, packetIdPub2);
    Serial.printf("Message: %.2f \n", temperature_Fahrenheit);
  }
}
