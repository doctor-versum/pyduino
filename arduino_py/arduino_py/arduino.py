import serial
import serial.tools.list_ports  # Füge diesen Import hinzu, um die seriellen Ports zu listen
import json
import time

DEBUG = False
LOGGING_LEVEL = {  # Logging-Level
    "ERROR": True,
    "WARNING": True,
    "IMPORTANT": True,
    "INFO": True
    }

EXPECTED_FIRMWARE = "0.1.1 Alpha"  # Erwartete Firmware-Version

# Reset
RESET = "\033[0m"

# Textfarben
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
BRIGHT_BLACK = "\033[90m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_WHITE = "\033[97m"

# Hintergrundfarben
BG_BLACK = "\033[40m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"
BG_BRIGHT_BLACK = "\033[100m"
BG_BRIGHT_RED = "\033[101m"
BG_BRIGHT_GREEN = "\033[102m"
BG_BRIGHT_YELLOW = "\033[103m"
BG_BRIGHT_BLUE = "\033[104m"
BG_BRIGHT_MAGENTA = "\033[105m"
BG_BRIGHT_CYAN = "\033[106m"
BG_BRIGHT_WHITE = "\033[107m"

# Textstile
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
BLINK = "\033[5m"
INVERT = "\033[7m"
HIDDEN = "\033[8m"
STRIKETHROUGH = "\033[9m"

class Management:
    """
    Manage the library settings. You DO NOT have to import this class. You only have to iport it, if you want to change the settings.
        
    Args:
        none

    Returns:
        none
    """
    def __init__(self):
        print(f"{BRIGHT_GREEN}Arduino Management System{RESET}")
    
    @staticmethod
    def list_ports():
        """
        List all available serial ports.
            
        Args:
            none

        Returns:
            list: A list of all available ports.
        """
        ports = serial.tools.list_ports.comports()
        Management.log(f"{BRIGHT_GREEN}Available ports:{RESET}", "INFO")
        for port in ports:
            Management.log(f"{BRIGHT_YELLOW}{port}{RESET}", "INFO")
        return ports

    def set_logging(self, state, custom={  # Logging-Level
                                        "ERROR": True,
                                        "WARNING": True,
                                        "IMPORTANT": True,
                                        "INFO": True
                                        }):
        """
        Set the logging level.

        Logging-Level:
        0: Logging disabled
        1: Logging errors only
        2: Logging errors and warnings
        3: Logging errors, warnings and important information
        4: Logging errors and important information
        5: Full logging
        6: Custom logging (you can customize, which logs you want to see using the custom parameter)
            
        Args:
            state (int): The logging level. Can be 0, 1, 2, 3, 4, 5 or 6.
            custom (dict): Custom logging level. Default is all enabled. You can set your own logging level with this parameter. Parameters:
                {
                    "ERROR": bool,
                    "WARNING": bool,
                    "IMPORTANT": bool,
                    "INFO": bool
                }

        Returns:
            none
        """
        global LOGGING_LEVEL
        if state >= 0 and state <= 6:
            if state == 0:
                print(f"{CYAN}Logging disabled{RESET}")
                LOGGING_LEVEL = {  # Logging-Level
                                "ERROR": False,
                                "WARNING": False,
                                "IMPORTANT": False,
                                "INFO": False
                                }
            elif state == 1:
                print(f"{CYAN}Logging errors only{RESET}")
                LOGGING_LEVEL = {  # Logging-Level
                                "ERROR": True,
                                "WARNING": False,
                                "IMPORTANT": False,
                                "INFO": False
                                }
            elif state == 2:
                print(f"{CYAN}Logging errors and warnings{RESET}")
                LOGGING_LEVEL = {  # Logging-Level
                                "ERROR": True,
                                "WARNING": True,
                                "IMPORTANT": False,
                                "INFO": False
                                }
            elif state == 3:
                print(f"{CYAN}Logging errors, warnings and important information{RESET}")
                LOGGING_LEVEL = {  # Logging-Level
                                "ERROR": True,
                                "WARNING": True,
                                "IMPORTANT": True,
                                "INFO": False
                                }
            elif state == 4:
                print(f"{CYAN}Logging errors and important information{RESET}")
                LOGGING_LEVEL = {  # Logging-Level
                                "ERROR": True,
                                "WARNING": False,
                                "IMPORTANT": True,
                                "INFO": False
                                }
            elif state == 5:
                print(f"{CYAN}Logging fully enabled{RESET}")
                LOGGING_LEVEL = {  # Logging-Level
                                "ERROR": True,
                                "WARNING": True,
                                "IMPORTANT": True,
                                "INFO": True
                                }
            elif state == 6:
                print(f"{CYAN}Custom Logging enabled{RESET}")
                LOGGING_LEVEL = custom

            print(f"{CYAN}The logging settings are:{RESET}")
            print(f"{CYAN}ERROR: {BLUE}{BOLD}{LOGGING_LEVEL['ERROR']}{RESET}")
            print(f"{CYAN}WARNING: {BLUE}{BOLD}{LOGGING_LEVEL['WARNING']}{RESET}")
            print(f"{CYAN}IMPORTANT: {BLUE}{BOLD}{LOGGING_LEVEL['IMPORTANT']}{RESET}")
            print(f"{CYAN}INFO: {BLUE}{BOLD}{LOGGING_LEVEL['INFO']}{RESET}")

    @staticmethod
    def log(message, level="INFO"):
        global LOGGING_LEVEL
        if LOGGING_LEVEL[level]:
            print(f"{message}")

class ArduinoUnoR3:
    """
    Initialize the Arduino Uno object.
        
    Args:
        port (str): The serial Port. Leave empty for auto-detection.
        baudrate (int): The baudrate. Default is 9600 and that is hardcoded into Firmware. You can change it, if you change it in the Arduino Firmware.
        pin_config (dict): Custom Pin-Configuration. You can leave this empty. It has to be a dictionary with the following structure:
        
            {
                "pin": "mode"
            }

            Example:
            {
                "3": "OUTPUT",
                "A0": "INPUT",
                "5": "INPUT_PULLUP"
            }

    Returns:
        none
    """
    last_port = None  # Klassenvariable zum Speichern des letzten Ports

    def __init__(self, port_input="AUTO", baudrate=9600, pin_config=None):
        if port_input == "AUTO":
            self.find_port(baudrate=baudrate)
        else:
            self.port = port_input

        if self.port is None:
            if ArduinoUnoR3.last_port is None:
                raise ValueError("No port set and no port history available")
            else:
                self.port = ArduinoUnoR3.last_port
        else:
            self.port = self.port
            ArduinoUnoR3.last_port = self.port  # Speichern des aktuellen Ports als letzten Port

        self.baudrate = baudrate
        self.ser = None
        self.pin_config = pin_config or {}

    def find_port(self, baudrate=9600):
        Management.log(f"{BRIGHT_GREEN}Auto-detecting serial port...{RESET}", "INFO")
        ports = Management.list_ports()
        port_final = None
        for port in ports:
            if "Arduino Uno" in port.description:
                Management.log(f"{BRIGHT_GREEN}Arduino found on port {port.device} ({port.description}){RESET}", "INFO")
                port_final = port.device
                break
        if port_final is None:
            Management.log(f"{RED}No Arduino found!{RESET}", "ERROR")
            exit()
        else:
            self.port = port_final

    def connect(self):
        """
        Initialize the connection to the Arduino.
            
        Args:
            none

        Returns:
            none
        """
        try:
            self.ser = serial.Serial(self.port, self.baudrate)
            time.sleep(2)  # Warten, damit die Verbindung stabil ist
            Management.log(f"{BRIGHT_GREEN}connected to device on serial port {self.port}{RESET}", "IMPORTANT")
            self.send_command("RESET", False)  # Setze Arduino zurück
            time.sleep(3)  # Warte, bis Arduino bereit ist
            response = self.send_command("PING", False)  # Teste die Verbindung
            if response == "RE PING":
                Management.log(f"{BRIGHT_GREEN}Arduino responds{RESET}", "IMPORTANT")
                if self.pin_config is not None:
                    data = self.pin_config
                else:
                    data = {}
                # Wandeln des Dicts in einen JSON-String
                json_string = json.dumps(data)
                # Senden des JSON-Strings über den seriellen Port
                self.ser.write(json_string.encode())  # encode() wandelt den String in Bytes um

                # Warten auf Antwort, die keinen Präfix "ACTION" hat
                while True:
                    if self.ser.in_waiting > 0:  # Warten auf eingehende Daten
                        response = self.ser.readline().decode().strip()  # Antwort vom Arduino lesen und dekodieren

                        if DEBUG:
                            print("Answer from Arduino: ", response)

                        # Wenn die Antwort mit "ACTION" beginnt, überspringen wir sie
                        if response.startswith("ACTION"):
                            continue  # Die Schleife geht zurück und wartet auf eine neue Antwort

                        if response == "SETUP FINISH":
                            Management.log(f"{BRIGHT_GREEN}Setup finished! Arduino fully connected.{RESET}", "IMPORTANT")
                            response = self.send_command("FIRMWARE", False)  # Firmware-Version abfragen
                            if response.startswith("RETURN"):
                                received = response[7:].strip()  # Bereinige die empfangene Firmware-Version
                                if received != EXPECTED_FIRMWARE:
                                    Management.log(f"{YELLOW}Unexpected firmware version on Arduino!{RESET}\n{BRIGHT_YELLOW}Expected: {EXPECTED_FIRMWARE}\nReceived: {received}{RESET}", "WARNING")
                                else:
                                    Management.log(f"{BRIGHT_GREEN}Arduino Firmware up-to-date!{RESET}", "INFO")
                            else:
                                Management.log(f"{RED}Error while reading firmware version!{RESET}", "ERROR")
                            break  # Setup abgeschlossen, Schleife verlassen
                        else:
                            Management.log(f"{RED}Error while setting up Arduino!{RESET}", "ERROR")
            else:
                Management.log(f"{RED}Arduino did not respond (correctly)!{RESET}\n{BRIGHT_RED}If you have the right port selected, please make sure, that the Arduino is using the provided Firmware.{RESET}", "ERROR")
        except serial.SerialException as e:
            Management.log(f"{RED}Error while connecting to Arduino: {ITALIC}{e}{RESET}\n{BRIGHT_RED}Please check the port and make sure, that the Arduino is connected.{RESET}", "ERROR")
            time.sleep(1)
            self.ser.close()
            self.connect()  # Erneut verbinden

    def check_for_reboot(self):
        if self.ser.in_waiting > 0:  # Prüfen, ob Daten verfügbar sind
            response = self.ser.readline().decode().strip()  # Antwort vom Arduino lesen und dekodieren
            if DEBUG:
                print("Antwort vom Arduino: ", response)

            if "REBOOT" in response:
                self.execute_reboot()

    def execute_reboot(self):
        self.ser.close()  # Verbindung trennen
        Management.log(f"{YELLOW} Arduino was reset and has to be set up again.{RESET}", "WARNING")
        time.sleep(1)
        self.connect()  # Erneut verbinden
        
    def disconnect(self):
        """
        disconnect from the Arduino.
            
        Args:
            none

        Returns:
            none
        """
        try:
            self.ser.close()
            Management.log(f"{YELLOW}disconnected from device on serial port {self.port}{RESET}", "WARNING")
        except Exception as e:
            raise Exception(f"Fehler: {e}")
        
    def send_command(self, command, check_reboot=True):
        """
        Send a command to the Arduino. Thhis is only needed, if you have added your own commands to the arduinos Firmware. Otherwise, you can ignore this function.
            
        Args:
            command (str): The command to send to the Arduino.
            check_reboot (bool): Check for a reboot of the Arduino. Default is True. I don't recommend changing this. It is only needed, if you force-reconnect the arduino.

        Returns:
            none
        """
        if check_reboot:
            self.check_for_reboot()  # Prüfen, ob der Arduino einen Neustart durchgeführt hat
        if self.ser and self.ser.is_open:
            self.ser.write((command + "\n").encode())  # Sende den Befehl an Arduino
            time.sleep(0.1)  # Kurze Pause, damit Arduino den Befehl verarbeiten kann
            response = self.ser.readline().decode().strip()
            if "REBOOT" in response and check_reboot:
                self.execute_reboot()
                response = "42"  # Dummy-Wert
            return response
        else:
            raise Exception("Not connected to Arduino")

    def set_digital_write(self, pin, state):
        """
        Set a digital pin to a specific state. Remember to set the pin to OUTPUT before using this function.
            
        Args:
            pin (int): The id of the pin.
            state (str): The state to set the pin to. Can be "HIGH" or "LOW".

        Returns:
            none
        """
        self.check_for_reboot()  # Prüfen, ob der Arduino einen Neustart durchgeführt hat
        command = f"DIGITALWRITE {pin} {state}"
        response = self.send_command(command)
        if DEBUG:
            print(response)

    def set_analog_write(self, pin, value):
        """
        Set an analog pin to a specific value. Remember to set the pin to OUTPUT before using this function.
            
        Args:
            pin (int): The id of the pin.
            value (int): The value to set the pin to. Can be between 0 and 255.

        Returns:
            none
        """
        self.check_for_reboot()  # Prüfen, ob der Arduino einen Neustart durchgeführt hat
        command = f"ANALOGWRITE {pin} {value}"
        response = self.send_command(command)
        if DEBUG:
            print(response)

    def get_digital_input(self, pin, isNumber=False):
        """
        Get the state of a digital pin. Remember to set the pin to INPUT or INPUT_PULLUP before using this function.
            
        Args:
            pin (int): The id of the pin.
            isNumber (bool): If True, the function will return 1 or 0. If False, the function will return "HIGH" or "LOW".

        Returns:
            int or str: The state of the pin.
        """
        self.check_for_reboot()  # Prüfen, ob der Arduino einen Neustart durchgeführt hat
        command = f"DIGITALINPUT {pin}"
        response = self.send_command(command)
        if response.startswith("RETURN"):
            value = int(response.split()[1])
            if isNumber:
                return value
            else:
                if value == 1:
                    return "HIGH"
                elif value == 0:
                    return "LOW"
        Management.log(f"{RED}Error while reading answer!{RESET}", "ERROR")
        return "ERROR"

    def get_analog_input(self, pin):
        """
        Get the state of an analog pin. Remember to set the pin to INPUT or INPUT_PULLUP before using this function.
            
        Args:
            pin (str): The id of the pin.

        Returns:
            int: The state of the pin.
        """
        self.check_for_reboot()  # Prüfen, ob der Arduino einen Neustart durchgeführt hat
        command = f"ANALOGINPUT {pin}"
        response = self.send_command(command)
        if response.startswith("RETURN"):
            return int(response.split()[1])
        else:
            Management.log(f"{RED}Error while reading answer!{RESET}", "ERROR")
            return 0

    def reset(self):
        """
        Force reset the Arduino.
            
        Args:
            none

        Returns:
            none
        """
        self.check_for_reboot()  # Prüfen, ob der Arduino einen Neustart durchgeführt hat
        command = "RESET"
        response = self.send_command(command)
        if DEBUG:
            print(response)