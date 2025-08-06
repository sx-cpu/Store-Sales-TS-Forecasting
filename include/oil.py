import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import plotly.express as px
from include.process import save_plot



class OilProcessor:
    def __init__(self, oil_df, temp_df, train_df, save_dir="res/oil"):
        self.oil = oil_df.copy()
        self.temp = temp_df.copy()
        self.train = train_df.copy()
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)

    
    def process(self):
        

        # Resamble
        self.oil = self.oil.set_index('date').dcoilwtico.resample("D").sum().reset_index()
        # Interpolate
        self.oil["dcoilwtico"] = np.where(self.oil.dcoilwtico==0, np.nan, self.oil.dcoilwtico)
        self.oil["dcoilwtico_interpolated"] = self.oil.dcoilwtico.interpolate()
        
        # Plot
        plotly_path = os.path.join(self.save_dir, 'Daily_Oil_Price.html')
        if os.path.exists(plotly_path):
            print(f"The line plot has already been saved as: {plotly_path}")
        
        else:
            p = self.oil.melt(id_vars=['date']+list(self.oil.columns[5:]), var_name='Legend')
            line = px.line(p.sort_values(['Legend', 'date'], ascending = [False, True]), 
                              x = 'date', y = 'value', color = 'Legend', title = "Daily Oil Price")
            
            save_plot(plotly_path, line)    
            
        # Correlation With Daily Oil Prices
        merged = pd.merge(self.temp, self.oil, how = "left")
        print("Correlation with Daily Oil Prices")
        print(merged.drop(["store_nbr", "dcoilwtico"], axis=1).corr("spearman").dcoilwtico_interpolated.loc[["sales", "transactions"]], "\n")
        

        scatter_path = os.path.join(self.save_dir, "oil_correlation.png")
        if os.path.exists(scatter_path):
            print(f"The scatter plot has already been saved as: {scatter_path}")
        
        else:
            fig, axes = plt.subplots(1, 2, figsize = (15,5))
            merged.plot.scatter(x = "dcoilwtico_interpolated",
                                y = "transactions", ax = axes[0])
            merged.plot.scatter(x = "dcoilwtico_interpolated", 
                        y = "sales", ax=axes[1], color = 'r')
            axes[0].set_title('Daily oil price & Transactions', fontsize = 15)
            axes[1].set_title('Daily oil price & Sales', fontsize = 15)

            plt.tight_layout()
            plt.savefig(scatter_path, dpi=300)
            print(f"The Picture has been saved as {scatter_path}")
      
      
      # Correlation between products families and sales
    def fam_sale_process(self):
          a = pd.merge(self.train.groupby(["date", "family"]).sales.sum().reset_index(),
                       self.oil.drop("dcoilwtico", axis=1),how = "left")
          c = a.groupby("family").corr("spearman").reset_index()
          c = c[c.level_1 == "dcoilwtico_interpolated"][["family", "sales"]].sort_values("sales")
          
          fig, axes = plt.subplots(7, 5, figsize = (20,20))
          for i, fam in enumerate(c.family):
              if i < 6:
                  a[a.family == fam].plot.scatter(x = "dcoilwtico_interpolated", 
                                                  y = "sales", ax=axes[0, i-1])
                  axes[0, i-1].set_title(fam+"\n Correlation:"+
                                         str(c[c.family == fam].sales.iloc[0])[:6], fontsize=12)
                  axes[0, i-1].axvline(x=70, color='r', linestyle='--')
              
              if i >= 6 and i < 11:
                  a[a.family == fam].plot.scatter(x = "dcoilwtico_interpolated", 
                                                  y = "sales", ax=axes[1, i-6])
                  axes[1, i-6].set_title(fam+"\n Correlation:"+
                                         str(c[c.family == fam].sales.iloc[0])[:6], fontsize = 12)
                  axes[1, i-6].axvline(x=70, color='r', linestyle='--')
              
              if i >= 11 and i < 16:
                  a[a.family == fam].plot.scatter(x = "dcoilwtico_interpolated", 
                                                  y = "sales", ax=axes[2, i-11])
                  axes[2, i-11].set_title(fam+"\n Correlation:"+
                                         str(c[c.family == fam].sales.iloc[0])[:6], fontsize = 12)
                  axes[2, i-11].axvline(x=70, color='r', linestyle='--')

              if i >= 16 and i < 21:
                  a[a.family == fam].plot.scatter(x = "dcoilwtico_interpolated", 
                                                  y = "sales", ax=axes[3, i-16])
                  axes[3, i-16].set_title(fam+"\n Correlation:"+
                                         str(c[c.family == fam].sales.iloc[0])[:6], fontsize = 12)
                  axes[3, i-16].axvline(x=70, color='r', linestyle='--')

              if i >= 21 and i < 26:
                  a[a.family == fam].plot.scatter(x = "dcoilwtico_interpolated", 
                                                  y = "sales", ax=axes[4, i-21])
                  axes[4, i-21].set_title(fam+"\n Correlation:"+
                                         str(c[c.family == fam].sales.iloc[0])[:6], fontsize = 12)
                  axes[4, i-21].axvline(x=70, color='r', linestyle='--')

              if i >= 26 and i < 31:
                  a[a.family == fam].plot.scatter(x = "dcoilwtico_interpolated", 
                                                  y = "sales", ax=axes[5, i-26])
                  axes[5, i-26].set_title(fam+"\n Correlation:"+
                                         str(c[c.family == fam].sales.iloc[0])[:6], fontsize = 12)
                  axes[5, i-26].axvline(x=70, color='r', linestyle='--')

              if i >= 31:
                  a[a.family == fam].plot.scatter(x = "dcoilwtico_interpolated", 
                                                  y = "sales", ax=axes[6, i-31])
                  axes[6, i-31].set_title(fam+"\n Correlation:"+
                                         str(c[c.family == fam].sales.iloc[0])[:6], fontsize = 12)
                  axes[6, i-31].axvline(x=70, color='r', linestyle='--')

          plt.tight_layout(pad=5)
          plt.suptitle("Daily Oil Product & Total Family Sales \n",
                        fontsize = 20)
          plot_path = os.path.join(self.save_dir, "fam_sale_cor.png")
          plt.savefig(plot_path, dpi=300)
          print(f"fam_sale_cor has been saved as {plot_path}")
                        
            
            
            
                  

                  


          
            


     
      
        
      

      


