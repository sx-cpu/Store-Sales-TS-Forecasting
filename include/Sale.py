import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os 
import plotly.express as px
from include.process import save_plot
import gc

class SalesProcessor:

    def __init__(self, train_df, save_dir="res/sales", remove = True, find_passive = True):
        self.train = train_df.copy()
        self.save_dir = save_dir
        
        if remove:
            self.remove_unopened()
        if find_passive:
            self.find_passive_family()

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
        

# ---------------------------------- forecast ---------------------------------
    
    def zero_forecasting(self):
        c = self.train.groupby(["store_nbr", "family"]).sales.sum().reset_index().sort_values(["family", "store_nbr"])
        c = c[c.sales == 0]

        # Anti join
        outer_join = self.train.merge(c[c.sales == 0].drop("sales", axis = 1), 
                                      how = 'outer', indicator=True)
        self.train = outer_join[~(outer_join._merge == 'both')].drop('_merge', axis = 1)
        del outer_join
        gc.collect()

        # predict
        zero_prediction = []
        for i in range(0, len(c)):
            zero_prediction.append(
                pd.DataFrame({
                    "date":pd.date_range("2017-08-16","2017-08-31").tolist(),
                    "store_nbr":c.store_nbr.iloc[i],
                    "family":c.family.iloc[i],
                    "sales":0
                })
            )
        zero_prediction = pd.concat(zero_prediction)
        del c
        gc.collect()


    # Use this function to check the passive family
    def find_passive_family(self):
        save_path = os.path.join(self.save_dir, "Store-Family.png")
        
        if os.path.exists(save_path):
            print(f"Store-Family plot already exists: {save_path}")
        else:
            c = self.train.groupby(["family", "store_nbr"]).tail(60).groupby(["family", "store_nbr"]).sales.sum().reset_index()
            print(c[c.sales == 0])

            # according to the output above:
            configs = [
                (10, "LAWN AND GARDEN"),
                (36, "LADIESWEAR"),
                (6, "SCHOOL AND OFFICE SUPPLIES"),
                (14, "BABY CARE"),
                (53, "BOOKS")
            ]
            fig, ax = plt.subplots(1, 5, figsize=(20, 4))
            for i, (store, family) in enumerate(configs):
                df = self.train[(self.train.store_nbr == store) & (self.train.family == family)]
                df.set_index("date").sales.plot(ax=ax[i], title=f"Store-{store} - {family}")
            plt.savefig(save_path)

    # Plot Daily Total Sales of the Family
    def Fam_Daily_total_sales(self):
        save_path = os.path.join(self.save_dir, "Daily_Total_Sales_of_the_family.png")
        a = self.train.set_index("date").groupby("family").resamble("D").sales.sum().reset_index()
        px.line(a, x = "date", y = "sales", color = "family", title = "Daily Total Sales of the Family")
        save_plot(save_path)

    # find the product preferred more
    def best_preferred(self):
        save_path = os.path.join(self.save_dir, "best_prefferd_family.png")
        a = self.train.groupby("family").sales.mean().sort_values(ascending = False).reset_index()
        px.bar(a, y="family", x="sales",color="family",title="Which product family preferred more?")
        save_plot(save_path)

    # How different can stores be from each other? 
    def store_diff(self):
        stores = pd.read_csv("./data/stores.csv")
        save_path = os.path.join(self.save_dir, "store_diff.png")
        d = pd.merge(self.train, stores)
        d["store_nbr"] = d["store_nbr"].astype("int8")
        d["year"] = d.date.dt.year
        px.line(d.groupby(["city", "year"]).sales.mean().reset_index(), x = "year", y = "sales", color = "city")
        save_plot(save_path)

        
        



        

        
    
    
    

