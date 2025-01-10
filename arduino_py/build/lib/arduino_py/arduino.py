import serial
import json
import time

class ArduinoUnoR3:
    last_port = None  # Klassenvariable zum Speichern des letzten Ports

    def __init__(self, port=None, baudrate=9600):
        if port is None:
            if ArduinoUnoR3.last_port is None:
                raise ValueError("Kein Port angegeben und kein letzter Port verfügbar")
            else:
                self.port = ArduinoUnoR3.last_port
        else:
            self.port = port
            ArduinoUnoR3.last_port = port  # Speichern des aktuellen Ports als letzten Port
        self.baudrate = baudrate
        self.ser = None

    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate)
            time.sleep(2)  # Warten, damit die Verbindung stabil ist
            print(f"Verbunden mit Arduino auf {self.port}")
            self.send_command("RESET", False)  # Setze Arduino zurück
            time.sleep(3)  # Warte, bis Arduino bereit ist
            response = self.send_command("PING", False)  # Teste die Verbindung
            if response == "RE PING":
                print("Arduino antwortet")
                data = {
                    "3": "OUTPUT",
                    "4": "OUTPUT",
                    "5": "OUTPUT",
                    "8": "INPUT",
                    "A0": "INPUT"
                }
                # Wandeln des Dicts in einen JSON-String
                json_string = json.dumps(data)
                # Senden des JSON-Strings über den seriellen Port
                self.ser.write(json_string.encode())  # encode() wandelt den String in Bytes um

                # Warten auf Antwort, die keinen Präfix "ACTION" hat
                while True:
                    if self.ser.in_waiting > 0:  # Warten auf eingehende Daten
                        response = self.ser.readline().decode().strip()  # Antwort vom Arduino lesen und dekodieren
                        print("Antwort vom Arduino: ", response)

                        # Wenn die Antwort mit "ACTION" beginnt, überspringen wir sie
                        if response.startswith("ACTION"):
                            continue  # Die Schleife geht zurück und wartet auf eine neue Antwort
                        
                        print("Antwort vom Arduino: ", response)

                        if response == "SETUP FINISH":
                            print("Arduino Setup abgeschlossen")
                            break  # Setup abgeschlossen, Schleife verlassen
                        else:
                            print("Fehler beim Setup")
            else:
                print("Fehler beim Verbinden mit Arduino")
        except serial.SerialException as e:
            print(f"Fehler beim Verbinden mit Arduino: {e}")

    def check_for_reboot(self):
        if self.ser.in_waiting > 0:  # Prüfen, ob Daten verfügbar sind
            response = self.ser.readline().decode().strip()  # Antwort vom Arduino lesen und dekodieren
            print("Antwort vom Arduino: ", response)

            if "REBOOT" in response:
                print("Arduino hat einen Neustart durchgeführt")
                self.connect()  # Erneut verbinden

    def disconnect(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Verbindung getrennt")
        else:
            raise Exception("Nicht mit Arduino verbunden")
        
    def send_command(self, command, check_reboot=True):
        if check_reboot:
            self.check_for_reboot()  # Prüfen, ob der Arduino einen Neustart durchgeführt hat
        if self.ser and self.ser.is_open:
            self.ser.write((command + "\n").encode())  # Sende den Befehl an Arduino
            time.sleep(0.1)  # Kurze Pause, damit Arduino den Befehl verarbeiten kann
            return self.ser.readline().decode().strip()  # Antwort von Arduino zurückgeben
        else:
            raise Exception("Nicht mit Arduino verbunden")

    def set_digital_write(self, pin, state):
        command = f"DIGITALWRITE {pin} {state}"
        response = self.send_command(command)
        print(response)

    def set_analog_write(self, pin, value):
        command = f"ANALOGWRITE {pin} {value}"
        response = self.send_command(command)
        print(response)

    def get_digital_input(self, pin):
        command = f"DIGITALINPUT {pin}"
        response = self.send_command(command)
        return response

    def get_analog_input(self, pin):
        command = f"ANALOGINPUT {pin}"
        response = self.send_command(command)
        return response

    def reset(self):
        command = "RESET"
        response = self.send_command(command)
        print(response)