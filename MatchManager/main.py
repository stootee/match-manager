import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.behaviors import ToggleButtonBehavior
from datetime import datetime
import time
import logging
import math
kivy.require('1.9.1')

"""
TODO:
    setup proper logging
    create squad management -- names in settings?
        how do we deal with two teams names?
    which half is it?
        are we into added / extra time?
    dynamic font sizes for clock and scores
    what should reset do?
    confirm before quit
    send to sns / log to s3
    sounds?
"""


class MainScreenManager(ScreenManager):
    _elapsedtime = NumericProperty(0)
    timestr = StringProperty()
    time_of_goal = StringProperty()
    _running = False
    _update = True
    _goals = []
    _home = NumericProperty(0)
    _away = NumericProperty(0)
    _h_scorers = ListProperty([])
    _a_scorers = ListProperty([])

    def __init__(self, **kwargs):
        super(MainScreenManager, self).__init__(**kwargs)
        self.increment_time(0)

    def record_who_scored(self):
        t = ToggleButtonBehavior.get_widgets('team')
        s = ToggleButtonBehavior.get_widgets('scorer')
        _team_who_scored = None
        _tws_name = None
        _person_who_scored = None
        time_of_goal = self.time_of_goal
        minutes = datetime.strptime(time_of_goal, '%H:%M:%S.%f')
        minutes = int(math.ceil((minutes - datetime(1900, 1, 1)).seconds / 60.0))

        for _t in t:
            if _t.state == 'down':
                _team_who_scored = _t.text
                _tws_name = _t.name

        for _s in s:
            if _s.state == 'down':
                _person_who_scored = _s.text

        if _team_who_scored and _person_who_scored:
            if _tws_name == 'home':
                self._home += 1
            else:
                self._away += 1

            if _tws_name == 'home':
                self._h_scorers.append('%s (%s)' % (_person_who_scored, minutes))
            else:
                self._a_scorers.append('%s (%s)' % (_person_who_scored, minutes))

            self._goals.append((_team_who_scored, _person_who_scored, time_of_goal),)
            self.current = 'manager_screen'
            self._update = True
            print self._goals
        else:
            popup = Popup(title='Missing Info',
                          content=Label(text='!'),
                          size_hint=(None, None), size=(self.width * 0.5, self.height * 0.5)
                          )
            popup.open()

    def _logger(self, log_details):
        print(run_uid, datetime.now().strftime('%Y%m%d %H:%M:%S'), log_details)

    def _set_time(self, elap):
        """ Set the time string to Hours:Minutes:Seconds """
        hours = int(elap / 3600)
        minutes = int((elap - hours * 3600) / 60)
        seconds = int((elap - hours * 3600) - minutes * 60.0)
        hseconds = int(((elap - hours * 3600) - minutes * 60.0 - seconds) * 100)
        display_minutes = int(elap / 60)
        if self._update:
            self.timestr = '%02d:%02d' % (display_minutes, seconds)
        return '%02d:%02d:%02d.%02d' % (hours, minutes, seconds, hseconds)

    def increment_time(self, interval):
        self._elapsedtime += interval
        self._set_time(self._elapsedtime)

    def _reset_timer(self):
        """ Reset the stopwatch. """
        self._logger(('RESET', self._set_time(self._elapsedtime)))
        self._elapsedtime = 0.0
        self._set_time(self._elapsedtime)

    def _start_timer(self):
        """ Start the stopwatch, ignore if running. """
        if not self._running:
            self._logger(('START', self._set_time(self._elapsedtime)))
            Clock.schedule_interval(self.increment_time, .01)
            self._running = 1

    def _stop_timer(self):
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:
            self._logger(('STOP', self._set_time(self._elapsedtime)))
            Clock.unschedule(self.increment_time, .1)
            self._running = 0


class ManagerBoxUI(Screen):
    def __init__(self, **kwargs):
        super(ManagerBoxUI, self).__init__(**kwargs)


class GoalScreen(Screen):
    def __init__(self, **kwargs):
        super(GoalScreen, self).__init__(**kwargs)


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
    def __init__(self, **kwargs):
        super(MatchManagerApp, self).__init__(**kwargs)

    def build(self):
        #Window.size = (300, 500)
        return root_widget

if __name__ == '__main__':
    root_widget = Builder.load_file('MatchManager.kv')
    run_uid = int(time.time())
    MatchManagerApp().run()
