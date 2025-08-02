# BASE
# ------------------------------------------------------
import numpy as np
import pandas as pd
import os
import gc
import warnings

# PACF - ACF
# ------------------------------------------------------
import statsmodels.api as sm

# DATA VISUALIZATION
# ------------------------------------------------------
import matplotlib.pyplot as plt
import seaborn as sns

import include.transactions as tr

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

# Datetime
train['date'] = pd.to_datetime(train.date)
test['date'] = pd.to_datetime(test.date)
transactions['date'] = pd.to_datetime(transactions.date)

#Data types
train.onpromotion = train.onpromotion.astype("float16")
train.sales = train.sales.astype("float32")
stores.cluster = stores.cluster.astype("int8")

line, box = tr.get_transactions(train, transactions, save_dir = "res/transactions")

