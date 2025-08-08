import pandas as pd
import numpy as np


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
    def __init__(self, train_df, test_df, stores_df):
        self.holidays = pd.read_csv("./data/holidays_events.csv")
        self.holidays.date = pd.to_datetime(self.holidays.date)
        self.train = train_df
        self.test = test_df
        self.store = stores_df
        self.Proc_Holidays()

    def Proc_Holidays(self):
        # Transferred Hollidays
        tr1 = self.holidays[(self.holidays.type == "Holidays") & 
                            (self.holidays.transferred == True)].drop("transferred", axis=1).reset_index(drop=True)
        tr2 = self.holidays[(self.holidays.type == "Transfer")].drop("transferred", axis=1).reset_index(drop=True)
        tr = pd.concat([tr1, tr2], axis=1)
        tr = tr.iloc[:, [5,1,2,3,4]]

        self.holidays = self.holidays[(self.holidays.type != "Transfer") & 
                                      (self.holidays.transferred == False)].drop("transferred", axis=1)
        self.holidays = pd.concat([self.holidays, tr]).reset_index(drop = True)
        
        # Additional Holidays
        self.holidays["description"] = self.holidays["description"].str.replace("-", "").str.replace("+","").str.replace('\d+',"")
        self.holidays["type"] = self.holidays["type"] = np.where(self.holidays["type"] == "Additional", "Holiday", self.holidays["type"])
        
        # Bridge Holidays
        self.holidays["description"] = self.holidays["description"].str.replace("Puente", "")
        self.holidays["type"] = np.where(self.holidays["type"] == "Bridge", "Holiday", self.holidays["type"])

        # Work Day Holidays, that is meant to payback the Bridge
        self.work_day = self.holidays[self.holidays.type == "Work Day"]
        self.holidays = self.holidays[self.holidays.type != "Work Day"]

    # Split
    def Split(self):
        self.events = self.holidays[self.holidays.type == "Event"].drop(["type","locale","locale_name"], axis=1).rename({"description":"events"}, axis = 1)
        self.holidays = self.holidays[self.holidays.type != "Event"].drop("type", axis=1)
        self.regional = self.holidays[self.holidays.type == "Regional"].rename({"locale_name":"state", "description":"holiday_regional"}, axis = 1).drop("locale", axis = 1).drop_duplicates()
        self.national = self.holidays[self.holidays.locale == "National"].rename({"description":"holiday_national"}, axis = 1).drop(["locale", "locale_name"], axis = 1).drop_duplicates()
        self.local = self.holidays[self.holidays.locale == "Local"].rename({"description":"holiday_local", "locale_name":"city"}, axis = 1).drop("locale", axis = 1).drop_duplicates()
        
        # National Holidays & Events 
        d = pd.merge(pd.concat([self.train, self.test]), self.stores)
        d["store_nbr"] = d["store_nbr"].astype("int8")

        d = pd.merge(d, self.national, how = 'left')
        d = pd.merge(d, self.regional, how = 'left', on = ["date", "state"])
        d = pd.merge(d, self.local, how = 'left', on = ["date", "city"])

        # Work Day: It will be removed when real work day column created
        d = pd.merge(d, self.work_day[["date", "type"]].rename({"type": "IsWorkDay"}, axis  = 1), how = "left")

        # Events
        self.events["events"] = np.where(self.events.events.str.contains("futbol"), "Futbol", self.events.events)
        


