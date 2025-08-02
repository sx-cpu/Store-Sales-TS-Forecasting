import pandas as pd


def get_transactions(train, transactions):
    temp = pd.merge(train.groupby(["date","store_nbr"]).sales.sum().reset_index(), transactions, how="left")