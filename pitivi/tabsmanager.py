# PiTiVi , Non-linear video editor
#
#       tabsmanager.py
#
# Copyright (c) 2005, Edward Hervey <bilboed@bilboed.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin St, Fifth Floor,
# Boston, MA 02110-1301, USA.

import gtk
from pitivi.utils.ui import SPACING


class BaseTabs(gtk.Notebook):
    def __init__(self, app):
        """ initialize """
        gtk.Notebook.__init__(self)
        self.set_border_width(SPACING)

        self.connect("create-window", self._createWindowCb)
        self.app = app
        self._createUi()

    def _createUi(self):
        """ set up the gui """
        settings = self.get_settings()
        settings.props.gtk_dnd_drag_threshold = 1
        self.set_tab_pos(gtk.POS_TOP)

    def append_page(self, child, label):
        gtk.Notebook.append_page(self, child, label)
        self._set_child_properties(child, label)
        child.show()
        label.show()

    def _set_child_properties(self, child, label):
        self.child_set_property(child, "detachable", True)
        self.child_set_property(child, "tab-expand", False)
        self.child_set_property(child, "tab-fill", True)
        label.props.xalign = 0.0

    def _detachedComponentWindowDestroyCb(self, window, child,
            original_position, label):
        notebook = window.child
        position = notebook.child_get_property(child, "position")
        notebook.remove_page(position)
        label = gtk.Label(label)
        self.insert_page(child, label, original_position)
        self._set_child_properties(child, label)
        self.child_set_property(child, "detachable", True)

    def _createWindowCb(self, from_notebook, child, x, y):
        original_position = self.child_get_property(child, "position")
        label = self.child_get_property(child, "tab-label")
        window = gtk.Window()
        window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_UTILITY)

        window.set_title(label)
        window.set_default_size(600, 400)
        window.connect("destroy", self._detachedComponentWindowDestroyCb,
                        child, original_position, label)
        notebook = gtk.Notebook()
        notebook.props.show_tabs = False
        window.add(notebook)

        window.show_all()
        # set_uposition is deprecated but what should I use instead?
        window.set_uposition(x, y)

        return notebook
