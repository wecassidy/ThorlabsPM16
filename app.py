"""
GUI interface to the Thorlabs PM16 series of power meters (or any
power meter with an that uses the same API as the PM16 class).

Written by: Wesley Cassidy
"""

import sys

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gio, GLib, Gtk

import PM16

import random
class FakePM16(PM16.PM16):
    """Generate a stream of random noise for testing."""

    def __init__(self, device):
        self.device = device
        self.FILE = None

    def power(self):
        """Retrun a random reading between 0 and 1 Watt"""
        return random.uniform(0, 1)

class App(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(
            self,
            application_id="ca.utoronto.electricatoms.PM16",
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )

        self.builder = None

        self.pm = FakePM16("")

    def do_activate(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("layout.glade")
        self.builder.connect_signals(self)

        window = self.builder.get_object("main-window")
        window.set_application(self)
        window.maximize()
        window.show()

        GLib.timeout_add(100, self.update_reading) # Update the reading every 100 ms

    def update_reading(self):
        reading = self.pm.power()

        # Format the output to nice units
        prefix = ""
        if reading < 1:
            unit_prefixes = iter(("m", "μ"))
            while reading < 1:
                # If there is a prefix for a 1e3 step down
                try:
                    prefix = next(unit_prefixes)
                except StopIteration:
                    break
                reading *= 1e3


        output_label = self.builder.get_object("power-output")
        output_label.set_text("{} {}W".format(reading, prefix))

        return True # Keep the timeout ticking

    def on_destroy(self, *args):
        Gtk.main_quit()

    def wavelength_set(self, *args):
        print(args)

if __name__ == "__main__":
    app = App()
    app.run(sys.argv)
