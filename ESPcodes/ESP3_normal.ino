#include <WiFi.h>
#include <PubSubClient.h>
// POUR FREQUENCE ET TEMPERATURE
#include <time.h>
#include <sys/time.h>
#include <esp_clk.h>

#ifdef __cplusplus
extern "C" {
#endif
uint8_t temprature_sens_read();
//uint8_t g_phyFuns;
#ifdef __cplusplus
}
#endif


// Paramètres de votre réseau WiFi
const char* ssid = "Capucine";
const char* password = "puyp4784";

// Paramètres du serveur MQTT
const char* mqtt_server = "192.168.230.78";
const int mqtt_port = 1883; // Port MQTT par défaut

const char* mqtt_topic = "BOUTON";
const char* mqtt_topic_tcpu3 = "TCPU3";
const char* mqtt_topic_fcpu3 = "FCPU3";
//déclaration moteur
const int in1Pin = 21;
const int in2Pin = 19;
const int enaPin = 5;
int motorSpeed = LOW;
int int1Speed = LOW;
int int2Speed = LOW;



WiFiClient espClient;
PubSubClient client(espClient);



void setup() {
  Serial.begin(115200);
  setupWiFi();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
  pinMode(in1Pin, OUTPUT); //config des pins
  pinMode(in2Pin, OUTPUT);
  pinMode(enaPin, OUTPUT);
}

// Declarations pour temperature
uint8_t temp_farenheit;
float temp_celsius;
char strftime_buf[64];
time_t now = 0;
struct tm timeinfo;
char buf[256];


void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
//moteur
  Serial.println(motorSpeed);
  digitalWrite(in1Pin, int1Speed); 
  digitalWrite(in2Pin, int2Speed);
  analogWrite(enaPin, 255);

 // Marche arrière
  digitalWrite(in1Pin, int1Speed); 
  digitalWrite(in2Pin, int2Speed);
  analogWrite(enaPin, 255);
  delay(1000);
      //TCPU
  localtime_r(&now, &timeinfo);
  strftime(strftime_buf, sizeof(strftime_buf), "%c", &timeinfo);
  sprintf(buf,"scan start %02d:%02d:%02d ",timeinfo.tm_hour,timeinfo.tm_min,timeinfo.tm_sec);
  Serial.print (buf);

  temp_farenheit= temprature_sens_read();
  temp_celsius = ( temp_farenheit - 32 ) / 1.8;
  Serial.print("Temp onBoard ");
  Serial.print(temp_farenheit);
  Serial.print("°F ");
  Serial.print(temp_celsius);
  Serial.println("°C");
    // Convertir le float en chaîne de caractères
  char temp_celsius_buffer[10]; // Dimensionnez le tampon en conséquence
  dtostrf(temp_celsius, 6, 2, temp_celsius_buffer);
  client.publish(mqtt_topic_tcpu3,temp_celsius_buffer);
 

  //FCPU
  // Obtenir la fréquence du processeur en MHz
  uint32_t cpuFreq = getCpuFrequencyMhz();
  Serial.print("Fréquence du processeur : ");
  Serial.print(cpuFreq);
  Serial.println(" MHz");
      // Convertir le float en chaîne de caractères
  char cpuFreq_buffer[10]; // Dimensionnez le tampon en conséquence
  dtostrf(cpuFreq, 6, 2, cpuFreq_buffer);
  client.publish(mqtt_topic_fcpu3,cpuFreq_buffer);

 // Attendre 5 secondes avant de répéter la lecture

}

void setupWiFi() {
  delay(10);
  Serial.println();
  Serial.print("Connexion à ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connecté");
  Serial.println("Adresse IP: ");
  Serial.println(WiFi.localIP());
}



void callback(char* topic, byte* payload, unsigned int length) {
  String message = "";
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  
  Serial.print("Message reçu [");
  Serial.print(topic);
  Serial.print("] ");
  Serial.println(message);
  Serial.println(motorSpeed);
  if (message == "on" && int1Speed == LOW ) {
    Serial.println(1);
    int1Speed = HIGH;
    int2Speed = HIGH; // Allumer le moteur
  } else {
    int1Speed = LOW;
    int2Speed = LOW;
    delay(1000);
  }
}



void reconnect() {
  while (!client.connected()) {
    Serial.print("Tentative de connexion MQTT...");
    String clientId = "ESP32Client2";
    clientId += String(random(0xffff), HEX);

    if (client.connect(clientId.c_str())) {
      Serial.println("connecté");
      client.subscribe(mqtt_topic); // S'abonner au sujet MQTT
    } else {
      Serial.print("échec, rc=");
      Serial.print(client.state());
      Serial.println(" Réessai dans 5 secondes...");
      delay(5000);
    }
  }
}
