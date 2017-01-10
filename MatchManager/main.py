import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, NumericProperty
from kivy.core.window import Window
from kivy.clock import Clock
from datetime import datetime
import time
import logging
kivy.require('1.9.1')

"""
TODO:
    setup proper logging
    create squad management UI
    send to sns / log to s3
    sounds?
"""


def _logger(log_details):
    print(run_uid, datetime.now().strftime('%Y%m%d %H:%M:%S'), log_details)


class ManagerBoxUI(Widget):
    def __init__(self, **kwargs):
        super(ManagerBoxUI, self).__init__(**kwargs)


class CPopup(Popup):
    def __init__(self, **kwargs):
        super(CPopup, self).__init__(**kwargs)


class ControlButtonsWidget(Widget):
    def __init__(self, **kwargs):
        super(ControlButtonsWidget, self).__init__(**kwargs)


class TimerOutputWidget(Widget):
    def __init__(self, **kwargs):
        super(TimerOutputWidget, self).__init__(**kwargs)


class GoalButtonWidget(Widget):
    def __init__(self, **kwargs):
        super(GoalButtonWidget, self).__init__(**kwargs)


class MatchManagerApp(App):
    _elapsedtime = NumericProperty()
    timestr = StringProperty()
    _running = False

    def __init__(self, **kwargs):
        super(MatchManagerApp, self).__init__(**kwargs)
        self.increment_time(0)

    def increment_time(self, interval):
        self._elapsedtime += interval

    def build(self):
        Window.size = (300, 300)
        manager = ManagerBoxUI()
        return manager

    def _set_time(self, elap):
        """ Set the time string to Hours:Minutes:Seconds """
        hours = int(elap / 360)
        minutes = int((elap - hours * 360) / 60)
        seconds = int((elap - hours * 360) - minutes * 60.0)
        hseconds = int(((elap - hours * 360) - minutes * 60.0 - seconds) * 100)
        self.timestr = '%02d : %02d : %02d' % (hours, minutes, seconds)
        return '%02d : %02d : %02d' % (hours, minutes, seconds)

    def _reset_timer(self):
        """ Reset the stopwatch. """
        _logger(('RESET', self._set_time(self._elapsedtime)))
        self._elapsedtime = 0.0
        self._set_time(self._elapsedtime)

    def _start_timer(self):
        """ Start the stopwatch, ignore if running. """
        if not self._running:
            _logger(('START', self._set_time(self._elapsedtime)))
            Clock.schedule_interval(self.increment_time, .01)
            self._running = 1

    def _stop_timer(self):
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:
            _logger(('STOP', self._set_time(self._elapsedtime)))
            Clock.unschedule(self.increment_time, .1)
            self._running = 0

    def goal_popup(self):
        which_side_scored = 'Home'
        if self._running:
            _logger(('GOAL:%s' % which_side_scored, self._set_time(self._elapsedtime)))
            p = CPopup(title="Goal!!", text="oooh, a goal")
            p.open()

    def start_popup(self):
        if not self._running:
            _logger('START' + '::' + self._set_time(self._elapsedtime))
            p = CPopup(title="Start", text='Test')
            p.open()



if __name__ == '__main__':
    run_uid = int(time.time())
    MatchManagerApp().run()
