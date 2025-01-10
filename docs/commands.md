# Commands

```
connect()
```
connect to the arduino

---

```
desconnect()
```
close the connection to the arduino

---

```
set_digital_write(pin, state)
```
set the digital state of a pin

pin (int): the pin, that you want to change. Make sure, you have set the pin to "OUTPUT", when connecting.
state (str): can either be "HIGH" or "LOW"

---

```
set_analog_write(pin, value)
```

set the analog value of a pin.

pin (int): the pin, that you want to change. Make sure, you have set the pin to "OUTPUT", when connecting.
value (int): The value to set the pin to. Can be between 0 and 255.

---

```
send_command(command, check_reboot)
```
Send a command to the Arduino. Thhis is only needed, if you have added your own commands to the arduinos Firmware. Otherwise, you can ignore this function.

command (str): The command to send to the Arduino.
check_reboot (bool): Check for a reboot of the Arduino. Default is True. I don't recommend changing this. It is only needed, if you force-reconnect the arduino.

---

```
get_digital_input(pin, isNumber)
```
Get the state of a digital pin. Remember to set the pin to INPUT or INPUT_PULLUP before using this function.

pin (int): The id of the pin.
isNumber (bool): If True, the function will return 1 or 0. If False, the function will return "HIGH" or "LOW".

Returns:
  int or str: The state of the pin.

---

```
get_analog_input(pin)
```
Get the state of an analog pin. Remember to set the pin to INPUT or INPUT_PULLUP before using this function.

pin (str): The id of the pin.

Returns:
  int: The state of the pin.

---

```
reset()
```
force-restarts the arduino.
