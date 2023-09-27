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
const char* ssid = "TP-Link_AB3E";
const char* password = "12831517";

// Paramètres du serveur MQTT
const char* mqtt_server = "192.168.230.78";
const int mqtt_port = 1883; // Port MQTT par défaut

const char* mqtt_topic = "BOUTON";
const char* mqtt_topic_tcpu2 = "TCPU2";
const char* mqtt_topic_fcpu2 = "FCPU2";
const char* mqtt_topic_lumino = "LUMINOSITE";
const int ledPin = 19;
const int DO_PIN = 35;

WiFiClient espClient;
PubSubClient client(espClient);



void setup() {

  Serial.begin(115200);
  setupWiFi();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
  pinMode(ledPin, OUTPUT); // Configuration de la broche de la LED comme sortie
  pinMode(DO_PIN, INPUT); // Config de la broche LDR

  

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

  // debut des mesures de lumière
  int lightValue = analogRead(DO_PIN); // Lit la valeur analogique de la photorésistance
  Serial.print("Luminosite : ");
  Serial.println(lightValue); // Affiche la valeur de luminosité sur le moniteur série
  char lightValue_buffer[10]; // Dimensionnez le tampon en conséquence
  dtostrf(lightValue, 6, 2, lightValue_buffer);
  client.publish(mqtt_topic_lumino, lightValue_buffer);
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
  client.publish(mqtt_topic_tcpu2,temp_celsius_buffer);
 

  //FCPU
  // Obtenir la fréquence du processeur en MHz
  uint32_t cpuFreq = getCpuFrequencyMhz();
  Serial.print("Fréquence du processeur : ");
  Serial.print(cpuFreq);
  Serial.println(" MHz");
      // Convertir le float en chaîne de caractères
  char cpuFreq_buffer[10]; // Dimensionnez le tampon en conséquence
  dtostrf(cpuFreq, 6, 2, cpuFreq_buffer);
  client.publish(mqtt_topic_fcpu2,cpuFreq_buffer);

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
  // Convertir le payload (message) en une chaîne de caractères
  String message = "";
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }

  Serial.print("Message reçu [");
  Serial.print(topic);
  Serial.print("] ");
  Serial.println(message);

  // Vérifier si le message est "on" pour allumer la LED
  if (message == "on" && digitalRead(ledPin)==LOW) {
    digitalWrite(ledPin, HIGH); // allumer la LED

    delay(1000); // Attend 1 seconde entre les lectures (ajustez selon vos besoins)
  } else  {
    digitalWrite(ledPin, LOW); // éteindre la LED
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
