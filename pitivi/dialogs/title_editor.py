# -*- coding: utf-8 -*-
# PiTiVi , Non-linear video editor
#
#       dialogs/title_editor.py
#
# Copyright (c) 2012, Jean-François Fortin Tam <nekohayo@gmail.com>
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
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import gtk
import os

from gettext import gettext as _

from pitivi.configure import get_ui_dir
from pitivi.dialogs.title_editor_canvas import TitlePreview


# FIXME: this is not used anywhere
#alignments = [
#        (0.0, 0.0), (0.5, 0.0), (1.0, 0.0),
#        (0.0, 0.5), (0.5, 0.5), (1.0, 0.5),
#        (0.0, 1.0), (0.5, 1.0), (1.0, 1.0)]

class TitleEditorDialog(object):

    def __init__(self, app, **kw):
        # **kw means any extra optional keyword arguments.
        # Here, we get those properties (or fallback to a default)
        self.text = kw.get('text', _("Hello! ☃"))
        self.font = kw.get('font', 'Sans')
        self.text_size = kw.get('text_size', 64)
        self.bg_color = kw.get('bg_color', (0, 0, 0, 1))
        self.fg_color = kw.get('fg_color', (1, 1, 1, 1))
        # Other default settings:
        self.x_alignment = 0.5
        self.y_alignment = 0.5

        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.join(get_ui_dir(), "texteditor.ui"))
        self.builder.connect_signals(self)

        self.window = self.builder.get_object("title_editor")
        self.preview_frame = self.builder.get_object("preview_frame")

        self.preview = TitlePreview(text=self.text)
        self.preview_frame.add(self.preview)
        # TODO: set preview_frame's aspect ratio
        self.preview.set_size_request(400, 300)

        self._textbuffer = self.builder.get_object("textview").get_buffer()
        self._textbuffer.connect('changed', self._bufferChangedCb)

        # FIXME: as soon as you try to get this widget connected, you get a MRO
        #self.builder.get_object("text_align").connect(self._textAlignCb)

    def _bufferChangedCb(self, widget):
        """
        When the user types in the textview, update the preview canvas.
        """
        text = widget.get_text(*widget.get_bounds())
        self.preview.props.text = text
        self.text = text

# FIXME: what's the point of this thing when we can set it at startup anyway?
#    def set(self, **kw):
#        self.__dict__.update(kw)

    def _fontButtonCb(self, widget):
        # Split from the end once, to separate the size from the font name
        font_string = widget.get_font_name().rsplit(None, 1)
        self.font, self.text_size = font_string[0], int(font_string[1])

    def _textAlignCb(self, widget):
        """
        This should set the text alignment type (left, center, right) within
        the text box, if possible and if supported by GStreamer.
        """
        raise NotImplementedError

    def _copy_to_dialog(self):
        """
        Set the dialog's widgets to match the initial values we have
        """
        self._textbuffer.set_text(self.text)
        font_button = self.builder.get_object("font_button")
        font_button.set_font_name('%s %d' % (self.font, self.text_size))

    def run(self):
        self.window.show_all()
        response = gtk.Dialog.run(self.window)
        # In the glade file, we set the OK button's response ID to 1.
        # Cancel is 0. If the dialog is closed by some other way, we get -4.
        if response == 1:
            print "Save the changes"
        self.window.destroy()
        return response
