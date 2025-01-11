#include <ArduinoJson.h>
#include <avr/wdt.h> // Watchdog-Bibliothek für Reset

// {"3":"OUTPUT", "4":"OUTPUT", "5":"OUTPUT", "8":"INPUT"}

const char* FIRMWARE_VERSION = "0.1.1 Alpha";

void setup() {
  // Start the serial communication
  Serial.begin(9600);
  while (!Serial) {
    // Wait for Serial to initialize (especially useful for boards like Leonardo)
  }

  // Send REBOOT message
  Serial.println("REBOOT");

  // Wait for "PING" command
  while (true) {
    if (Serial.available()) {
      String input = Serial.readStringUntil('\n');
      input.trim(); // Remove any extra whitespace or newline characters

      if (input == "PING") {
        Serial.println("RE PING");
        break;
      }
    }
  }

  // Wait for configuration in JSON format
  while (true) {
    if (Serial.available()) {
      String jsonConfig = Serial.readStringUntil('\n');
      jsonConfig.trim();

      // Parse JSON to configure pins
      StaticJsonDocument<512> doc; // Adjust size as needed
      DeserializationError error = deserializeJson(doc, jsonConfig);

      if (error) {
        Serial.println("ERROR Invalid JSON");
        continue; // Wait for a valid JSON configuration
      }

      // Iterate through the JSON object and configure pins
      for (JsonPair keyValue : doc.as<JsonObject>()) {
        const char* key = keyValue.key().c_str(); // Get the key as a C-string
        int pin = atoi(key); // Convert the key to an integer
        String mode = keyValue.value().as<String>();
        Serial.println("ACTION Pinmode for " + String(pin) + ": " + mode);

        if (mode == "INPUT") {
          pinMode(pin, INPUT);
        } else if (mode == "OUTPUT") {
          pinMode(pin, OUTPUT);
          digitalWrite(pin, LOW);
        } else if (mode == "INPUT_PULLUP") {
          pinMode(pin, INPUT_PULLUP);
        } else {
          Serial.println("ERROR Invalid mode for pin " + String(pin));
        }
      }

      // Setup complete
      Serial.println("SETUP FINISH");
      break;
    }
  }
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // Befehl bis Zeilenende lesen
    command.trim(); // Entfernt Leerzeichen und Zeilenumbrüche
    handleCommand(command); // Befehl verarbeiten
  }
}

// Funktion zur Verarbeitung der Befehle
void handleCommand(String command) {
  if (command.startsWith("DIGITALWRITE")) {
    setDigitalWrite(command);
  }
  else if (command.startsWith("ANALOGWRITE")) {
    setAnalogWrite(command);
  }
  else if (command.startsWith("DIGITALINPUT")) {
    getDigitalInput(command);
  }
  else if (command.startsWith("ANALOGINPUT")) {
    getAnalogInput(command);
  }
  else if (command.startsWith("FREQUENCY")) {
    setFrequency(command);
  }
  else if (command.startsWith("FIRMWARE")) {
    getFirmware(command);
  }
  else if (command.equals("RESET")) {
    Serial.println("ACTION reset");
    delay(100); // Nachricht abschließen
    resetController();
  } 
  else {
    Serial.println("ERROR Unbekannter Befehl: " + command);
  }
}

void getFirmware(String command) {
  Serial.println("RETURN " + String(FIRMWARE_VERSION));
}

void setDigitalWrite(String command) {
  int space1 = command.indexOf(' ');  // Finde erstes Leerzeichen
  int space2 = command.indexOf(' ', space1 + 1); // Finde zweites Leerzeichen

  int pin = command.substring(space1 + 1, space2).toInt(); // Extrahiere den Pin
  if (pin < 0 || pin > 13) {
    Serial.println("ERROR Ungültiger Pin: " + String(pin));
    return;
  }

  String value = command.substring(space2 + 1); // Extrahiere HIGH/LOW
  if (value.equalsIgnoreCase("HIGH")) {
    digitalWrite(pin, HIGH);
    Serial.println("ACTION Pin " + String(pin) + " auf HIGH gesetzt.");
  } 
  else if (value.equalsIgnoreCase("LOW")) {
    digitalWrite(pin, LOW);
    Serial.println("ACTION Pin " + String(pin) + " auf LOW gesetzt.");
  } 
  else {
    Serial.println("ERROR Ungültiger Wert. Verwenden Sie HIGH oder LOW.");
  }
}

void setAnalogWrite(String command) {
  int space1 = command.indexOf(' ');  // Finde erstes Leerzeichen
  int space2 = command.indexOf(' ', space1 + 1); // Finde zweites Leerzeichen
  
  int pin = command.substring(space1 + 1, space2).toInt(); // Extrahiere den Pin
  String value = command.substring(space2 + 1); // Extrahiere den Wert

  // Analoger Wert (PWM-Wert von 0 bis 255)
  int analogValue = value.toInt();

  // Überprüfe, ob der Pin ein PWM-fähiger Pin ist (Arduino Uno Pins 3, 5, 6, 9, 10, 11)
  if (pin == 3 || pin == 5 || pin == 6 || pin == 9 || pin == 10 || pin == 11) {
    if (analogValue >= 0 && analogValue <= 255) {
      analogWrite(pin, analogValue);  // PWM-Wert setzen
      Serial.println("ACTION PWM-Wert " + String(analogValue) + " an Pin " + String(pin) + " gesetzt.");
    } 
    else {
      Serial.println("ERROR Ungültiger PWM-Wert. Verwenden Sie einen Wert zwischen 0 und 255.");
    }
  } else {
    Serial.println("ERROR Ungültiger PWM-Pin: " + String(pin));
  }
}

void setFrequency(String command) {
  int space1 = command.indexOf(' ');  // Finde erstes Leerzeichen
  int space2 = command.indexOf(' ', space1 + 1); // Finde zweites Leerzeichen
  int space3 = command.indexOf(' ', space2 + 1); // Finde drittes Leerzeichen
  
  int pin = command.substring(space1 + 1, space2).toInt(); // Extrahiere den Pin
  int analogValue = command.substring(space2 + 1, space3).toInt();
  int length = command.substring(space3 + 1).toInt();

  // Überprüfe, ob der Pin ein PWM-fähiger Pin ist (Arduino Uno Pins 3, 5, 6, 9, 10, 11)
  if (pin == 3 || pin == 5 || pin == 6 || pin == 9 || pin == 10 || pin == 11) {
    if (analogValue > 0) {
      if (length > 0) {
        tone(pin, analogValue, length);  // PWM-Wert setzen
        Serial.println("ACTION Frequency " + String(analogValue) + " at Pin " + String(pin) + " set for " + String(length) + ".");
      } else {
        tone(pin, analogValue);
        Serial.println("ACTION Frequency " + String(analogValue) + " at Pin " + String(pin) + " set.");
      }
    } else {
      noTone(pin);
      Serial.println("ACTION Stopped Pin " + String(pin) + ".");
    }
  } else {
    Serial.println("ERROR Ungültiger PWM-Pin: " + String(pin));
  }
}

// Funktion: DigitalInput holen
void getDigitalInput(String command) {
  int space1 = command.indexOf(' ');  // Finde erstes Leerzeichen

  int pin = command.substring(space1).toInt(); // Extrahiere den Pin

  Serial.println("RETURN " + digitalRead(pin));
}

void getAnalogInput(String command) {
  int space1 = command.indexOf(' ');  // Finde erstes Leerzeichen

  String pinString = command.substring(space1 + 1); // Extrahiere den Pin (z.B. A0)
  
  // Überprüfe, ob der Pin mit 'A' beginnt und entferne das 'A'
  if (pinString.charAt(0) == 'A') {
    pinString = pinString.substring(1); // Entferne das 'A'
  }
  
  int pin = pinString.toInt(); // Extrahiere die Zahl des Pins
  
  // Wandelt den analogen Pin (0 bis 5) auf den tatsächlichen Pin (14 bis 19) um
  if (pin >= 0 && pin <= 5) {
    pin = 14 + pin;  // A0 -> 14, A1 -> 15, ..., A5 -> 19
  } else {
    Serial.println("ERROR Ungültiger Analog-Pin: " + String(pin));
    return;
  }

  int value = analogRead(pin); // Lese den analogen Wert
  Serial.println("RETURN " + String(value)); // Gebe den Wert zurück
}

void resetController() {
  wdt_enable(WDTO_15MS); // Watchdog-Timer auf 15 ms einstellen
  while (true) {
    // Warten, bis der Watchdog-Timer den Reset auslöst
  }
}