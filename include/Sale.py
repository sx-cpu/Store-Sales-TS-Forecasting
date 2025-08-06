import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os 
import plotly.express as px
from include.process import save_plot
import gc

class SalesProcessor:

    def __init__(self, train_df, save_dir="res/sales"):
        self.train = train_df.copy()
        self.save_dir = save_dir
        self.remove_unopened()

# Correlations among stores
    def cormat_plot(self):
        os.makedirs(self.save_dir, exist_ok = True)
        save_path = os.path.join(self.save_dir, "cormat.png")

        if os.path.exists(save_path):
            print(f"Heatmap already exists: {save_path}")

        else:
            a = self.train[["store_nbr", "sales"]]
            a["ind"] = 1
            a["ind"] = a.groupby("store_nbr").ind.cumsum().values
            a = pd.pivot(a, index = "ind", columns = "store_nbr", 
                        values = "sales").corr()
            mask = np.triu(np.ones_like(a, dtype=bool))
            plt.figure(figsize=(20, 20))
            sns.heatmap(a,
                        annot=True,
                        fmt='.1f',
                        cmap='coolwarm',
                        square=True,
                        mask=mask,
                        linewidths=1,
                        cbar=False)
            plt.title("Correlations among stores", fontsize=20)
            plt.savefig(save_path, dpi=300)
            print(f"Heatmap has been saved as {save_path}")

    # Daily total sales of the stores
    def daily_total_sales(self):
        os.makedirs(self.save_dir, exist_ok=True)
        save_path = os.path.join(self.save_dir, "Daily_total_sales_of_the_stores.html")
        
        if os.path.exists(save_path):
            print(f"Daily total sales of the stores already exists: {save_path}")
        else:
            a = self.train.set_index("date").groupby("store_nbr").resample("D").sales.sum().reset_index()
            line = px.line(a, x = "date", y = "sales", 
                        color = "store_nbr", title = "Daily total sales of the stores")
            save_plot(save_path, line)

    # While you are looking at the time series of the stores one by one, you may find some of the stores have no sales 
    # at the beginning of 2013. In the following codes, we will get rid of them.
    def remove_unopened(self):
        self.train = self.train[~((self.train.store_nbr == 52) & (self.train.date < "2017-04-20"))]
        self.train = self.train[~((self.train.store_nbr == 22) & (self.train.date < "2015-10-09"))]
        self.train = self.train[~((self.train.store_nbr == 42) & (self.train.date < "2015-08-21"))]
        self.train = self.train[~((self.train.store_nbr == 21) & (self.train.date < "2015-07-24"))]
        self.train = self.train[~((self.train.store_nbr == 29) & (self.train.date < "2015-03-20"))]
        self.train = self.train[~((self.train.store_nbr == 20) & (self.train.date < "2015-02-13"))]
        self.train = self.train[~((self.train.store_nbr == 53) & (self.train.date < "2014-05-29"))]
        self.train = self.train[~((self.train.store_nbr == 36) & (self.train.date < "2013-05-09"))]
        
        

        
    
    
    

