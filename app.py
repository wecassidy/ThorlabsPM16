"""
GUI interface to the Thorlabs PM16 series of power meters (or any
power meter with an that uses the same API as the PM16 class).

Written by: Wesley Cassidy
"""

import sys

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gio, Gtk

class App(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(
            self,
            application_id="ca.utoronto.electricatoms.PM16",
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )

        self.builder = None

    def do_activate(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("layout.glade")
        self.builder.connect_signals(self)

        window = self.builder.get_object("main-window")
        window.set_application(self)
        window.maximize()
        window.show()

    def on_destroy(self, *args):
        Gtk.main_quit()

    def wavelength_set(self, *args):
        print(args)

if __name__ == "__main__":
    app = App()
    app.run(sys.argv)
