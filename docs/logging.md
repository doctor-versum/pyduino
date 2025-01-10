# Logging system

This is a custom logging system. Compatibility with the logging library will be added later, but for now, it will remain as is. There are different logging levels, depending on what you want to see.

# Usage:

First, import the management module, if you haven't already:
```
from pyduino import Management
settings = Management()
```

Then, you can change the logging settings like this:
```
settings.set_logging(5)
```

# Levels

**Level 0:**
This will disable all logging. You won't get anything from the library.

**Level 1:**
You will only get errors. No warnings, no plain info, no debug, nothing.

**Level 2:**
This will log all errors and warnings.

**Level 3:**
This will print all errors, warnings, and also important information, like connections, ports, and similar things.

**Level 4:**
This will only log errors and important information, not warnings.

**Level 5:**
Logging fully enabled.

**Level 6:**
With this, you can add a second parameter, which allows you to customize what you get. This has to be in JSON format. Here is a template:
```
{
	"ERROR": bool,
	"WARNING": bool,
	"IMPORTANT": bool,
	"INFO": bool
}
```
Custom levels can be set like this:
```
settings.set_logging(6, {
    "ERROR": True,
    "WARNING": True,
    "IMPORTANT": True,
    "INFO": True
})
```
