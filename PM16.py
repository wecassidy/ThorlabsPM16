"""
Simple interface to the Thorlabs PM16 power meter.

Tested on PM16-121, but likely works for all PM16 meters (and possibly
other Thorlabs power meters).

How to use:
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

Known issues: reads and writes to the power meter will sometimes start
timing out. The only solution to this seems to be to unplug and plug
back in the power meter and re-initialize the PM16 object.

Note: Thorlabs, as far as I can tell, doesn't publicly document the
USBTMC interface for their power meters. The USBTMC commands in this
class were copied from
https://github.com/djorlando24/pyLabDataLogger/blob/master/src/device/usbtmcDevice.py#L285.
"""

import time, os

class USBTMC:
    """
    Simple implememntation of a USBTMC device driver, in the style of
    visa.h
    """
    def __init__(self, device):
        self.device = device
        self.FILE = os.open(device, os.O_RDWR)

        # TODO: Test that the file opened

    def write(self, command):
        os.write(self.FILE, command.encode());

    def read(self, length = 4000):
        return os.read(self.FILE, length).decode("utf-8")

    def query(self, command, length = 4000):
    	self.write(command)
    	return self.read(length)

    def getName(self):
        self.write("*IDN?")
        return self.read(300)

    def sendReset(self):
        self.write("*RST")

    def close(self):
        os.close(self.FILE)

class PM16(USBTMC):
    """
    Simple interface to the Thorlabs PM16 power meter.
    """

    def __init__(self, device):
        super().__init__(device)

    def power(self):
        """Read the power from the meter in Watts."""
        return float(self.query("Read?"))

    def stream(self, samples=None, duration=None, delay=0.5):
        """
        Continuously poll the power meter and print the results.

        samples: the number of samples to read before stopping. Optional, default infinite.
        duration: the length of time to poll for. Optional, default infinite.
        delay: the time between samples, in seconds. Optional, default 0.5 s

        If neither samples or duration are provided to limit the poll,
        this method will keep reading until keyboard interrupt. At any
        time, keyboard interrupt will cleanly stop the poll.

        Returns all values read during the poll.
        """
        log = []
        poll_start = time.time()
        while (samples is None and duration is None) or (samples is not None and len(log) < samples) or (duration is not None and time.time() - poll_start < duration):
            try:
                val = self.read()
                print("{:.3f} mW".format(val*1e3))
                log.append(val)
                time.sleep(delay)
            except KeyboardInterrupt:
                pass

        return log
