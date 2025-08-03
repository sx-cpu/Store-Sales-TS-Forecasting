
import numpy as np
import pandas as pd
import warnings
import include.transactions as tr
import include.oil as o


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


# process transactions
tr.get_transactions(transactions, temp, save_dir = "res/transactions")
o.get_oil(oil, temp, save_dir = "res/oil")