# pyduino
This is a work-in-progress python library to control a connected arduino over serial.

# Supported devices:

- Arduino Uno R3
  - fully supported
 
- Any other Arduino and Arduino-like device
  - probably works, but there is no garatee. Also, the automatic port detection only works with arduino unos.

# Usage

first, upload the Arduino remote firmware to the arduino. Open the Arduino IDE on your system of choice and open the Project. You can change some varibeles at the top, but it is NOT recommendet, if you don't know, what you are doing. Then, just press upload.

then, import ArduinoUnoR3 module:

```
from arduino_py import ArduinoUnoR3
arduino = ArduinoUnoR3()
```

and lastly, connect to the Arduino:

```
arduino.connect()
```

Thats it. there is more you can do, but thats all, you have to do, to get the library to work.

# Optional

import the Management module:

```
from arduino_py import Management
settings = Management()
```
and now, you can change the logging and probably later also some other settings.
```
settigns.set_logging(5)
```
A full explenation on, what every level does, is available in the documentation.
