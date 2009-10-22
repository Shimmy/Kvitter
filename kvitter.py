#!/usr/bin/env python

import sys, cgi, os
import gtk
import gobject

gobject.threads_init()
try:
    import pygtk
    pygtk.require("2.16")
except:
    pass
try:
    import gtk.glade
except:
    sys.exit(1)


if __name__ == "__main__":
    from app import KvitterApp
    app = KvitterApp()
    app.run()
    gtk.main()

