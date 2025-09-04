# src/time_manager.py

import time as pytime

last_tick = pytime.time()
tick_interval = 2.0  # кожна секунда = 1 хвилина в грі

class TimeManager:
    def __init__(self, profile_time):
        self.day = profile_time["day"]
        self.hour = profile_time["hour"]
        self.minute = profile_time.get("minute", 0)

    def tick(self, minutes=1):
        self.minute += minutes
        if self.minute >= 60:
            self.minute -= 60
            self.hour += 1
        if self.hour >= 24:
            self.hour = 0
            self.day += 1

    def get_weekday(self):
        weekdays = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"]
        return weekdays[(self.day - 1) % 7]

    def get_time_str(self):
        return f"{self.hour:02d}:{self.minute:02d}"

    def export(self):
        return {"day": self.day, "hour": self.hour, "minute": self.minute}

