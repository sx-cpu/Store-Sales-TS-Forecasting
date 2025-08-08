
import numpy as np
import pandas as pd
import warnings
from include.transactions import TransactionsProcessor
from include.oil import OilProcessor
from include.Sale import SalesProcessor
from include.HolidaysEvents import HolidaysEventsProcessor



# CONFIGURATIONS
# ------------------------------------------------------
pd.set_option('display.max_columns', None)
pd.options.display.float_format = '{:.2f}'.format
warnings.filterwarnings('ignore')


# DATASET
# ------------------------------------------------------
train = pd.read_csv("./data/train.csv")
test = pd.read_csv("./data/test.csv")
stores = pd.read_csv("./data/stores.csv")
transactions = pd.read_csv("./data/transactions.csv").sort_values(["store_nbr","date"])
oil = pd.read_csv("./data/oil.csv")



# Datetime
train['date'] = pd.to_datetime(train.date)
test['date'] = pd.to_datetime(test.date)
transactions['date'] = pd.to_datetime(transactions.date)
oil["date"] = pd.to_datetime(oil.date)

#Data types
train.onpromotion = train.onpromotion.astype("float16")
train.sales = train.sales.astype("float32")
stores.cluster = stores.cluster.astype("int8")

# temp is a dataframe that contains the total sales and transactions for each store and date
temp = pd.merge(train.groupby(["date", "store_nbr"]).sales.sum().reset_index(),
                     transactions, how = "left")


#---------------------------------Analysis-----------------------------

# process transactions
processor_transactions=TransactionsProcessor(transactions, temp, save_dir = "res/transactions")
processor_transactions.process()
# process oil
processor_oil = OilProcessor(oil, temp, train, save_dir ="res/oil")
processor_oil.process()
processor_oil.fam_sale_process()

# process sales
processor_sales = SalesProcessor(train, save_dir = "res/sales")
processor_sales.cormat_plot()
processor_sales.daily_total_sales()

# HolidaysEventsProcess
processor_Holi = HolidaysEventsProcessor(train, test, stores)



#----------------------------------Forecast------------------------------

# Zero Forecasting
# (You don't need the machine learning or deep learning or another things for these time series
# because we had some simple time series.)
processor_sales.zero_forecasting()