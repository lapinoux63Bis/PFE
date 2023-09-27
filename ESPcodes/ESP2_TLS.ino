#include <WiFiClientSecure.h>
#include <TBPubSubClient.h>
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
const char* password = "12831517";


// Paramètres du serveur MQTT
IPAddress mqtt_server(192, 168, 230, 78);
const int mqtt_port = 8883; // Port MQTT par défaut

//déclarations des certificats
const char* ca_cert = \
                      "-----BEGIN CERTIFICATE-----\n" \
                      "MIIDazCCAlOgAwIBAgIUDKkmCxCl2/MV5tfs7w0rCmQvoCYwDQYJKoZIhvcNAQEL\n" \
                      "BQAwRTELMAkGA1UEBhMCRlIxEzARBgNVBAgMClNvbWUtU3RhdGUxDDAKBgNVBAoM\n" \
                      "A1BGRTETMBEGA1UEAwwKUEZFX2Jyb2tlcjAeFw0yMzA5MjAwOTQ4NTJaFw0zMzA5\n" \
                      "MTcwOTQ4NTJaMEUxCzAJBgNVBAYTAkZSMRMwEQYDVQQIDApTb21lLVN0YXRlMQww\n" \
                      "CgYDVQQKDANQRkUxEzARBgNVBAMMClBGRV9icm9rZXIwggEiMA0GCSqGSIb3DQEB\n" \
                      "AQUAA4IBDwAwggEKAoIBAQCjpUvIhQWqmUUPOn5MPmngv6GsdifeolnvDP+mcQPt\n" \
                      "XjSSbfRBeB5P5xGyWILLj5h5Bjcack9MOGmsWRAh890PWbup/KviEffXgl0nyZRn\n" \
                      "EYWJHSRO8fqHCIUP9NHKwrKNHzJAlC9E6CkGBiyFMR5+MLRbdm/061RtVDhlFpXi\n" \
                      "ELvbATdHSSKhRLgiAyFzetWmIe3krGRSTSYxkK656hJO+qbKph/tS42IZHyq6TaA\n" \
                      "BcUSBetDi2Fd/IhjrGsslsAoWV9GE5nR4yM6ZGgEXfjncLBPQkET+YYILuQtX//I\n" \
                      "iT30g70XW27/3YuGHCCZFtevRajckFQpG2jvyCF2sU9hAgMBAAGjUzBRMB0GA1Ud\n" \
                      "DgQWBBQCXBiOq5BDQdkzDXRl4DushuPthDAfBgNVHSMEGDAWgBQCXBiOq5BDQdkz\n" \
                      "DXRl4DushuPthDAPBgNVHRMBAf8EBTADAQH/MA0GCSqGSIb3DQEBCwUAA4IBAQBC\n" \
                      "WR648pGR3JCZ+1PxIDB0GuOR3LalhF1yLqsAEmtsSqHfeEx9vHy2Re0VtgZvYG9r\n" \
                      "pFsx/y4+iU/KasBlUWqI7rtbIarH+Qyookqgcw+N+ZY5LKlzGgHlNxH2pfuNFXsr\n" \
                      "XqYP3MYK0KcbidrI6pMLL+UoqbYQNChpeknN5EjyoULzAs+O5etuYnUmprzEaR5X\n" \
                      "PIm1jBpCAy9/l6WPsBKDhzs8EHteCk1XNdallvRCmtVIrOPvRawpYRiji8iRuC31\n" \
                      "BQ+0lm1Q1DQwmFWMHTnw9CQTg+mNj47sXygrlctUMzzwYxeIlT80hNBd5QP9Vdlk\n" \
                      "zzDSGQkW1U2/T+3H62Pl\n" \
                      "-----END CERTIFICATE-----\n";

const char* client_cert = \
                          "-----BEGIN CERTIFICATE-----\n" \
                          "MIIDIzCCAgsCFD7teQDOLfpU8Z/CQ2ZR31lGjbtRMA0GCSqGSIb3DQEBCwUAMEUx\n" \
                          "CzAJBgNVBAYTAkZSMRMwEQYDVQQIDApTb21lLVN0YXRlMQwwCgYDVQQKDANQRkUx\n" \
                          "EzARBgNVBAMMClBGRV9icm9rZXIwHhcNMjMwOTIwMDk1MTEzWhcNMjUwOTA5MDk1\n" \
                          "MTEzWjBXMQswCQYDVQQGEwJGUjETMBEGA1UECAwKU29tZS1TdGF0ZTEhMB8GA1UE\n" \
                          "CgwYSW50ZXJuZXQgV2lkZ2l0cyBQdHkgTHRkMRAwDgYDVQQDDAdjbGllbnQxMIIB\n" \
                          "IjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvdHRAvXLSV4eQUZ9KWi78jSZ\n" \
                          "fGIKVS9OkfkrsrdNhvvO7/Z0YNbHPxDBmjVbhdQfUHE9cepS8+wR7gH0k6OcEOA6\n" \
                          "A0R6RzzSASIFDlQcsuxvcf6jmmyokdpCWu1gm2tvbxCnyDzFL2XOsmordf3G2zS0\n" \
                          "/6DAFi6smIj04+tv7dwZJRcBNjxM5D1IV27ckszlM/eBBSNSZ/KTRhORrN3QGVpS\n" \
                          "ZagzstKx29Up/v48rjH87tDRjmFdPshhBofsUoXQ5c868uKwIFROpHrelgRuypLW\n" \
                          "b36hhAeimW/S+Bci9mzRJ9cPgnnCWZcbtymUxlQvZnf8LggoiJUcH6YRPHIKIwID\n" \
                          "AQABMA0GCSqGSIb3DQEBCwUAA4IBAQCTSFZhvtjJSu8MpfOCM2hl8KKVTNuhvPAe\n" \
                          "c8+3dK9iMEfagvGiy9oP220PRWxIrkFzdR1zlEj3p9/7h5fKNMn+L1YnnaarS/TF\n" \
                          "syG/biwloJBC1BFLFucprM+hQuoz4aV2qQfznw4OW3j4c0Z1EG3dQcN+Bh1+xTVU\n" \
                          "mTXCY+tMSpKPtJoWhoBs2rZNBu3Ypb7IuLwX7PjXazvnDoWkAlQMaUoP893udBtT\n" \
                          "Y8ZN51oBoKaQgFNPcqWL8YRmQTL4174u0Ny7ItoPuJyPsFzhaUSNG8uGCgITPV3p\n" \
                          "73kGZAVY0+jJZyjbCJ32BbGnpeJAicJa8Oqnf9HAyrODdV+sQyeW\n" \
                          "-----END CERTIFICATE-----\n";

const char* client_key = \
                         "-----BEGIN RSA PRIVATE KEY-----\n" \
                         "MIIEpQIBAAKCAQEAvdHRAvXLSV4eQUZ9KWi78jSZfGIKVS9OkfkrsrdNhvvO7/Z0\n" \
                         "YNbHPxDBmjVbhdQfUHE9cepS8+wR7gH0k6OcEOA6A0R6RzzSASIFDlQcsuxvcf6j\n" \
                         "mmyokdpCWu1gm2tvbxCnyDzFL2XOsmordf3G2zS0/6DAFi6smIj04+tv7dwZJRcB\n" \
                         "NjxM5D1IV27ckszlM/eBBSNSZ/KTRhORrN3QGVpSZagzstKx29Up/v48rjH87tDR\n" \
                         "jmFdPshhBofsUoXQ5c868uKwIFROpHrelgRuypLWb36hhAeimW/S+Bci9mzRJ9cP\n" \
                         "gnnCWZcbtymUxlQvZnf8LggoiJUcH6YRPHIKIwIDAQABAoIBAF4sNCflzd8uZJA5\n" \
                         "6mqa3XPCiMte0IWGnNJq7jUSH9JyJy6B9Sb+J4ewRny9MBTrMkX0iGl1uYXufs64\n" \
                         "BaEhsJHmzKFGXevtzrplKGD9deeGyZuim4RHmDIUOItn7V/uIzDU8Ii1LZbgSXXW\n" \
                         "mo1FRF0Ifyu7ktDugw6CFAznh3ZXuSBBGXaV4U/mL19F5yFie9x2SiWsonH/mRDW\n" \
                         "iT7Vo5KX50pTZiCup61V1OVDVD/9RuhKZQQ43cxYUT+AERzYOcS0n/kjBRSyxEVS\n" \
                         "x3whjG5G/SbXmdyPVVZ00sz3mqVwD1M//zFYGYuKL7Q77ULnV+KMn8LQa5h7jsdh\n" \
                         "DPeXKwECgYEA/Efga4GKRjRHaVSCDsnbh8Qxi/pkGWoiArZ5yWwogva3f8Yz5IwV\n" \
                         "p7nA7N/4ykunZqtgvrJZJxmNRR9tC/X8f/PIno/Kv7+g5LehEm9fmSDE12AxvgWH\n" \
                         "cg2QSqc34GH5o3zUEOm6ugCTlsSfsjaICOunUsbm7Nbl/jWxXfQbneMCgYEAwJ41\n" \
                         "G1aAbHZclEe2wbpxXPDl4y9iXHr41lk2p2C7E8hcu8WmuksvzSUTKofxMy58O/0q\n" \
                         "BTvCZ5TofMOt8vuqaWStVd+lHBP7ev6KzcgPE1yV7O+soBBfQ2m7djlj2nfE2jbJ\n" \
                         "uA4VSbt7dHT5dPirCzTo7O5BAe0/AOqKM0D/lsECgYEAwFlNEqrB8qUJjZWRVBUz\n" \
                         "/F/qJv/SMk5pgAgA80Iz4Saa4iEMj8T+/dLy9agO2K62A+HG8Z6putYQkBNV4Ti8\n" \
                         "PBJzc/HOdER3N+uKM7QW/3msm0oMowU0MBGHYmP8hmgtHimexwZuCENIRDvGRuqs\n" \
                         "7aA/Ay4EA7AVy6zEfw4PwGECgYEAnwJ76OOSBPf5GVfSYT9e0lD0FoZJdvr1bU4c\n" \
                         "tjQ+e+hN1Z0nNGdZQMs4dUXgMlZPrN4j0EozBHuDKWwIr6xeU78O8PM9RF6injh/\n" \
                         "sb1T5LHr+rspEMIzQl2IqeJaskFpOpM8FztZC5NAKTVfsdaOrSOyndVZyRNnjYQR\n" \
                         "Lpqb5IECgYEAyHghK5bzaYzVmzIm2jghqMbReaB/Eu3OMJyCDq2IPySNUhPJQ0vL\n" \
                         "BFTrYx+sKtc2xzqAu03W3H0D0fl25HJ9u2FbNqhYJ1u8DOkIwppuJipr3jWkzd5d\n" \
                         "XcSU3ob5RehbO9V0z/foTe4DGbYgqpiy5mToKYtzjzbp4EuCNMwTGsA=\n" \
                         "-----END RSA PRIVATE KEY-----\n";

const char* mqtt_topic = "BOUTON";
const char* mqtt_topic_tcpu2 = "TCPU2";
const char* mqtt_topic_fcpu2 = "FCPU2";
const char* mqtt_topic_lumino = "LUMINOSITE";
const int ledPin = 19;
const int DO_PIN = 35;

// Declarations pour temperature
uint8_t temp_farenheit;
float temp_celsius;
char strftime_buf[64];
time_t now = 0;
struct tm timeinfo;
char buf[256];

WiFiClientSecure espClient;
PubSubClient client(espClient);

void setup() {

  Serial.begin(115200);
  setupWiFi();
    //setup certificates for TLS
  espClient.setCACert(ca_cert);
  espClient.setCertificate(client_cert);
  espClient.setPrivateKey(client_key);
  client.setServer(mqtt_server, mqtt_port);

  while (!client.connected()) {
    Serial.println("Tentative de connexion au broker MQTT...");
    //verifyFingerprint();
    if (client.connect("ESP32Client_2")) {  //PAS SUR DE CA
      Serial.println("Connecté au broker MQTT");
    } else {
      Serial.print("Échec de la connexion au broker MQTT, rc=");
      Serial.print(client.state());
      Serial.println(" Réessayer dans 5 secondes");
      delay(5000);
    }
  }
  pinMode(ledPin, OUTPUT); // Configuration de la broche de la LED comme sortie
  digitalWrite(ledPin, HIGH);
  pinMode(DO_PIN, INPUT); // Config de la broche LDR
  client.subscribe(mqtt_topic);
}

void loop() {
    
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  client.setCallback(callback);
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
    String clientId = "ESP32Client_2";
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