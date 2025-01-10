# Logging system

This is a custom logging system. I will be adding compatibility with the logging library later, but for now, it will be just this. There are different levels, depending on, what you want to see.

# Usage:

first, import the management module, if you havn't already:
```
from arduino_py import Management
settings = Management()
```

then, you can change the logging settings like this:
```
settings.set_logging(5)
```

# Levels

**Level 0:**
This will disable all logging. You won't get anythign from the library.

**Level 1:**
You will only get Errors. no warnings, no plain info, no debug, nothing.

**Level 2:**
This will log all errors and warnings.

**Level 3:**
This will print all errors, warnings and also important information, like connections, ports and similar things.

**Level 4:**
This will only log errors and important information. not warnigns.

**Level 5:**
Logging fully enabled.

**Level 6:**
With this, you can add a second parameter, which allows you to customize, what you get. THis has to be in json. here is a template:
```
{
	"ERROR": bool,
	"WARNING": bool,
	"IMPORTANT": bool,
	"INFO": bool
}
```
Custem levels can be set like this:
```
settings.set_logging(6,{
                        "ERROR": True,
                        "WARNING": True,
                        "IMPORTANT": True,
                        "INFO": True
                        })
```
