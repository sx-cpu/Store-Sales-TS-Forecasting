import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from include.process import save_plot


def get_oil(oil, temp, save_dir):

    temp = pd.merge(temp, oil, how = "left")
    
    # Resamble
    oil = oil.set_index('date').dcoilwtico.resample("D").sum().reset_index()
    # Interpolate
    oil["dcoilwtico"] = np.where(oil.dcoilwtico==0, np.nan, oil.dcoilwtico)
    oil["dcoilwtico_interpolated"] = oil.dcoilwtico.interpolate()
    # Plot
    p = oil.melt(id_vars=['date']+list(oil.keys()[5:]), var_name='Legend')
    line = px.line(p.sort_values(['Legend', 'date'], ascending = [False, True]), 
                   x = 'date', y = 'value', color = 'Legend', title = "Daily Oil Price")
    
    save_plot(save_dir, line, 'Daily_Oil_Price.html')


    # Correlation With Daily Oil Prices
    print("Correlation with Daily Oil Prices")
    print(temp.drop(["store_nbr", "dcoilwtico"], axis=1).
          corr("Spearman").dcoilwtico_interpolated.loc[["sales", "transactions"]], "\n")
    
    fig, axes = plt.subplots(1, 2, figsize = (15,5))
    temp.plot.scatter(x = "dcoilwtico_interpolated",
                       y = "transactions", ax = axes[0])
    temp.plot.scatter(x = "dcoilwtico_interpolated", 
                      y = "sales", ax=axes[1], color = 'r')
    axes[0].set_title('Daily oil price & Transactions', fontsize = 15)
    axes[1].set_title('Daily oil price & Sales', fontsize = 15)
    
    






    return line



