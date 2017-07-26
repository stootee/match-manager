#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
TODO:
    setup proper logging
    create squad management UI
    send to sns / log to s3
    sounds?
"""

from Tkinter import Tk, BOTH, StringVar, NO, X
from ttk import Frame, Button, Style, Label
import tkMessageBox
from datetime import datetime
import time


def _logger(log_details):
    print(run_uid, datetime.now().strftime('%Y%m%d %H:%M:%S'), log_details)
    

class ManagerUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        # make Esc exit the program
        self.parent.bind('<Escape>', lambda e: self._quit_timer())
        self._start = 0.0
        self._elapsedtime = 0.0
        self._running = 0
        self.style = None
        self.timestr = StringVar()
        self.init_ui()

    def timer_widget(self):
        """ Make the time lable. """
        l = Label(
            self,
            textvariable=self.timestr,
            background="White",
            font=('Helvetica', 32),
            anchor='center',
            relief='sunken'
        )
        self._set_time(self._elapsedtime)
        l.pack(fill=X, expand=NO, pady=50, padx=50)

    def control_button_widget(self):
        frame = Frame(self, style='button.TFrame', padding=10)
        frame.pack(side='top', fill=BOTH)

        buttons = Button(frame, text="Start", command=self._start_timer)
        buttons.pack(padx=5, side='left')
        buttons = Button(frame, text="Stop", command=self._stop_timer)
        buttons.pack(padx=5, side='left')
        buttons = Button(frame, text="Reset", command=self._reset_timer)
        buttons.pack(padx=5, side='left')
        buttons = Button(frame, text="Quit", command=self._quit_timer)
        buttons.pack(padx=5, side='left')

    def goal_button_widget(self):
        frame = Frame(self)
        frame.pack(padx=0, pady=0, side='top')

        buttons = Button(frame, text="Home Goal", command=lambda: self._goal_scored('home'), style="goal.TButton")
        buttons.pack(padx=5, pady=20, side='top')
        buttons = Button(frame, text="Away Goal", command=lambda: self._goal_scored('away'), style="goal.TButton")
        buttons.pack(padx=5, pady=20, side='top')

    def _update(self):
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
        self._set_time(self._elapsedtime)
        self._timer = self.after(50, self._update)

    def _set_time(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        minutes = int(elap / 60)
        seconds = int(elap - minutes * 60.0)
        hseconds = int((elap - minutes * 60.0 - seconds) * 100)
        self.timestr.set('%02d:%02d' % (minutes, seconds))
        return '%02d:%02d:%02d' % (minutes, seconds, hseconds)

    def _reset_timer(self):
        """ Reset the stopwatch. """
        _logger(('RESET', self._set_time(self._elapsedtime)))
        self._start = time.time()
        self._elapsedtime = 0.0
        self._set_time(self._elapsedtime)

    def _start_timer(self):
        """ Start the stopwatch, ignore if running. """
        if not self._running:
            _logger(('START', self._set_time(self._elapsedtime)))
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1

    def _stop_timer(self):
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:
            _logger(('STOP', self._set_time(self._elapsedtime)))
            self.after_cancel(self._timer)
            self._elapsedtime = time.time() - self._start
            self._set_time(self._elapsedtime)
            self._running = 0

    def _goal_scored(self, which_side_scored):
        if self._running:
            _logger(('GOAL:%s' % which_side_scored, self._set_time(self._elapsedtime)))
            tkMessageBox.showinfo(
                "%s Goal!!!" % which_side_scored,
                self._set_time(self._elapsedtime)
            )

    def _quit_timer(self):
        ans = tkMessageBox.askokcancel("", "Quit the app?", icon="warning")
        if ans:
            _logger(('QUIT:yes', self._set_time(self._elapsedtime)))
            self.parent.destroy()
        else:
            _logger(('QUIT:no', self._set_time(self._elapsedtime)))

    def init_ui(self):
        self.parent.title("Match Manager")
        self.style = Style()
        self.style.theme_use("clam")
        self.style.configure('TButton', width=10, padx=5, pady=5)
        self.style.configure('button.TFrame', background="Grey")
        self.style.configure('goal.TButton', font=('Helvetica', 24), width=10, relief="raised")

        self.pack(fill=BOTH, expand=1)

        self.control_button_widget()

        self.timer_widget()

        self.goal_button_widget()


def main():
    window_width = 360
    window_height = 500

    root = Tk()
    root.geometry("%dx%d+100+100" % (window_width, window_height))

    ManagerUI(root)
    root.mainloop()


if __name__ == '__main__':
    run_uid = int(time.time())
    main()
