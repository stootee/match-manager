import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
import time
import logging
kivy.require('1.9.1')


def _logger(log_details):
    logging.info(run_uid, datetime.now().strftime('%Y%m%d %H:%M:%S'), log_details)


class ManagerBoxUI(Widget):
    def __init__(self, **kwargs):
        super(ManagerBoxUI, self).__init__(**kwargs)

        self._start = 0.0
        self._elapsedtime = 0.0
        self._running = 0
        self.style = None
        self.timestr = None

    # def timer_widget(self):
    #     """ Make the time label. """
    #     l = Label(
    #         self,
    #         textvariable=self.timestr,
    #         background="White",
    #         font=('Helvetica', 32),
    #         anchor='center',
    #         relief='sunken'
    #     )
    #     self._set_time(self._elapsedtime)
    #     l.pack(fill=X, expand=NO, pady=50, padx=50)

    # def control_button_widget(self):
    #     frame = Frame(self, style='button.TFrame', padding=10)
    #     frame.pack(side='top', fill=BOTH)
    #
    #     buttons = Button(frame, text="Start", command=self._start_timer)
    #     buttons.pack(padx=5, side='left')
    #     buttons = Button(frame, text="Stop", command=self._stop_timer)
    #     buttons.pack(padx=5, side='left')
    #     buttons = Button(frame, text="Reset", command=self._reset_timer)
    #     buttons.pack(padx=5, side='left')
    #     buttons = Button(frame, text="Quit", command=self._quit_timer)
    #     buttons.pack(padx=5, side='left')

    # def goal_button_widget(self):
    #     frame = Frame(self)
    #     frame.pack(padx=0, pady=0, side='top')
    #
    #     buttons = Button(frame, text="Home Goal", command=lambda: self._goal_scored('home'), style="goal.TButton")
    #     buttons.pack(padx=5, pady=20, side='top')
    #     buttons = Button(frame, text="Away Goal", command=lambda: self._goal_scored('away'), style="goal.TButton")
    #     buttons.pack(padx=5, pady=20, side='top')

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

    def _reset_timer(self, a):
        """ Reset the stopwatch. """
        _logger(('RESET', self._set_time(self._elapsedtime)))
        self._start = time.time()
        self._elapsedtime = 0.0
        self._set_time(self._elapsedtime)

    def _start_timer(self, a):
        """ Start the stopwatch, ignore if running. """
        if not self._running:
            _logger(('START', self._set_time(self._elapsedtime)))
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1

    def _stop_timer(self, a):
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:
            _logger(('STOP', self._set_time(self._elapsedtime)))
            self.after_cancel(self._timer)
            self._elapsedtime = time.time() - self._start
            self._set_time(self._elapsedtime)
            self._running = 0

    def _goal_scored(self, a, which_side_scored):
        if self._running:
            _logger(('GOAL:%s' % which_side_scored, self._set_time(self._elapsedtime)))


class CPopup(Popup):
    def __init__(self, **kwargs):
        super(CPopup, self).__init__(**kwargs)


class ControlButtonsWidget(Widget):
    def __init__(self, **kwargs):
        super(ControlButtonsWidget, self).__init__(**kwargs)

    def popup(self):
        p = CPopup()
        p.open()


class TimerOutputWidget(Widget):
    def __init__(self, **kwargs):
        super(TimerOutputWidget, self).__init__(**kwargs)


class GoalScoredWidget(Widget):
    def __init__(self, **kwargs):
        super(GoalScoredWidget, self).__init__(**kwargs)

    def _goal_scored(self, which_side_scored):
        #if self._running:
        _logger(('GOAL:%s' % which_side_scored, self._set_time(self._elapsedtime)))


class MatchManagerApp(App):

    def build(self):
        manager = ManagerBoxUI()
        return manager


if __name__ == '__main__':
    run_uid = int(time.time())
    MatchManagerApp().run()
