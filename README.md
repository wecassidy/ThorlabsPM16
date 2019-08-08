# ThorlabsPM16
Simple Python interface to the Thorlabs PM16 power meter.

Tested on PM16-121, but likely works for all PM16 meters (and possibly
other Thorlabs power meters).

## How to use
```python
>>> import PM16
>>> pm = PM16("/dev/usbtmc0") # Replace with whatever USBTMC port the meter is attached to
>>> pm.read() # Power as a float, in W
1.5692888e-02
>>> values = pm.stream() # Poll the power meter until keyboard interrupt
15.365363 mW
15.674598 mW
15.663893 mW
15.513761 mW
...
# keyboard interrupt
>>> values
[1.5365363e-02, 1.5674598e-02, 1.5663893e-02, 1.5513761e-02, ...]
```

## Known issues
reads and writes to the power meter will sometimes start
timing out. The only solution to this seems to be to unplug and plug
back in the power meter and re-initialize the PM16 object.

Note: Thorlabs, as far as I can tell, doesn't publicly document the
USBTMC interface for their power meters. The USBTMC commands in this
class were copied from
[djorlando24/pyLabDataLogger](https://github.com/djorlando24/pyLabDataLogger/blob/master/src/device/usbtmcDevice.py#L285).
