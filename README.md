# ThorlabsPM16
Simple Python interface to the Thorlabs PM16 power meter.

Tested on PM16-121, but likely works for all PM16 meters (and possibly
other Thorlabs power meters).

## How to use
```python
>>> import PM16
>>> pm = PM16("/dev/usbtmc0") # Replace with whatever USBTMC port the meter is attached to
Current wavelength: 780 nm
>>> pm.set_wavelength(684) # Change wavelength to 684 nm
>>> pm.power() # Power as a float, in W
1.5692888e-02
>>> values = pm.stream() # Poll the power meter until keyboard interrupt
2.6368066 mW
2.7559481 mW
2.8252213 mW
...
# keyboard interrupt
>>> values
[0.0026368066, 0.0027559481, 0.0028252213, ...]
```

## Known issues
Reading from the power meter when there is nothing available leads to
that read and any further commands failing with a `TimeoutError`. To
fix this, unplug the power meter and re-initialize the `PM16` object.

Note: Thorlabs, as far as I can tell, doesn't publicly document the
USBTMC interface for their power meters. The USBTMC commands in this
class were copied from
[djorlando24/pyLabDataLogger](https://github.com/djorlando24/pyLabDataLogger/blob/master/src/device/usbtmcDevice.py#L285).
