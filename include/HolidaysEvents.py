import pandas as pd


# It contains a lot of information inside but, don't worry. You just need to take a breathe and think! 
# It is a meta-data so you have to split it logically and make the data useful.
# What are our problems?
# 1. Some national holidays have been transferred.
# 2. There might be a few holidays in one day. When we merged all of data, number of rows might increase. We don't want duplicates.
# 3. What is the scope of holidays? It can be regional or national or local. You need to split them by the scope.
# 4. Work day issue
# 5. Some specific events
# 6. Creating new features etc.
class HolidaysEventsProcessor:
    def __init__(self):
        self.holidays = pd.read_csv("../data/holidays_events.csv")
        self.holidays.date = pd.to_datetime(self.holidays.date)
