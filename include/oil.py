import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import plotly.express as px
from include.process import save_plot



class OilProcessor:
    def __init__(self, oil_df, temp_df, save_dir="res/oil"):
        self.oil = oil_df.copy()
        self.temp = temp_df.copy()
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
     
      
        
      

      


