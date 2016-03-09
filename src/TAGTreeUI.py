"""
Created on 08.03.2016

@author: Albert
"""

from tkinter import IntVar, Menu, Tk
from nltk.util import in_idle
from nltk.draw.util import CanvasFrame
from nltk.draw.tree import TreeWidget


class TAGTreeUI(object):
    """
    This class is based on code from the nltk draw(tree) module:
    # Copyright (C) 2001-2015 NLTK Project
    # Author: Edward Loper <edloper@gmail.com>
    # URL: <http://nltk.org/>
    redistributed and modified under http://www.apache.org/licenses/LICENSE-2.0 by Benjamin Kosmehl
    """


    def __init__(self, *trees):
        from math import sqrt, ceil

        self._trees = trees

        self._top = Tk()
        self._top.title('NLTK')
        self._top.bind('<Control-x>', self.destroy)
        self._top.bind('<Control-q>', self.destroy)

        cf = self._cframe = CanvasFrame(self._top)
        self._top.bind('<Control-p>', self._cframe.print_to_file)

        # Size is variable.
        self._size = IntVar(self._top)
        self._size.set(12)
        bold = ('helvetica', -self._size.get(), 'bold')
        helv = ('helvetica', -self._size.get())

        # Lay the trees out in a square.
        self._width = int(ceil(sqrt(len(trees))))
        self._widgets = []
        for i in range(len(trees)):
            widget = TreeWidget(cf.canvas(), trees[i], node_font=bold,
                                leaf_color='#008040', node_color='#004080',
                                roof_color='#004040', roof_fill='white',
                                line_color='#004040', draggable=1,
                                leaf_font=helv)
            widget.bind_click_trees(widget.toggle_collapsed)
            self._widgets.append(widget)
            cf.add_widget(widget, 0, 0)

        self._layout()
        self._cframe.pack(expand=1, fill='both')
        self._init_menubar()

    def _layout(self):
        i = x = y = ymax = 0
        width = self._width
        for i in range(len(self._widgets)):
            widget = self._widgets[i]
            (oldx, oldy) = widget.bbox()[:2]
            if i % width == 0:
                y = ymax
                x = 0
            widget.move(x-oldx, y-oldy)
            x = widget.bbox()[2] + 10
            ymax = max(ymax, widget.bbox()[3] + 10)

    def _init_menubar(self):
        menubar = Menu(self._top)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label='Print to Postscript', underline=0,
                             command=self._cframe.print_to_file,
                             accelerator='Ctrl-p')
        filemenu.add_command(label='Exit', underline=1,
                             command=self.destroy, accelerator='Ctrl-x')
        menubar.add_cascade(label='File', underline=0, menu=filemenu)

        zoommenu = Menu(menubar, tearoff=0)
        zoommenu.add_radiobutton(label='Tiny', variable=self._size,
                                 underline=0, value=10, command=self.resize)
        zoommenu.add_radiobutton(label='Small', variable=self._size,
                                 underline=0, value=12, command=self.resize)
        zoommenu.add_radiobutton(label='Medium', variable=self._size,
                                 underline=0, value=14, command=self.resize)
        zoommenu.add_radiobutton(label='Large', variable=self._size,
                                 underline=0, value=28, command=self.resize)
        zoommenu.add_radiobutton(label='Huge', variable=self._size,
                                 underline=0, value=50, command=self.resize)
        menubar.add_cascade(label='Zoom', underline=0, menu=zoommenu)

        self._top.config(menu=menubar)

    def resize(self, *e):
        bold = ('helvetica', -self._size.get(), 'bold')
        helv = ('helvetica', -self._size.get())
        xspace = self._size.get()
        yspace = self._size.get()
        for widget in self._widgets:
            widget['node_font'] = bold
            widget['leaf_font'] = helv
            widget['xspace'] = xspace
            widget['yspace'] = yspace
            if self._size.get() < 20: widget['line_width'] = 1
            elif self._size.get() < 30: widget['line_width'] = 2
            else: widget['line_width'] = 3
        self._layout()

    def destroy(self, *e):
        if self._top is None: return
        self._top.destroy()
        self._top = None

    def mainloop(self, *args, **kwargs):
        """
        Enter the Tkinter mainloop.  This function must be called if
        this demo is created from a non-interactive program (e.g.
        from a secript); otherwise, the demo will close as soon as
        the script completes.
        """
        if in_idle(): return
        self._top.mainloop(*args, **kwargs)