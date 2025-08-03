import pandas as pd
import plotly.express as px
import os
from include.process import save_plot


def get_transactions(transactions, temp, save_dir="res/transactions"):

    # Spearman correlation between Total Sales and Transactions 
    
    print("Spearman Correlation between Total Sales and Transactions: {:,.4f}".format(
        temp.corr("spearman").sales.loc["transactions"]))
    
    # line chart
    line = px.line(transactions.sort_values(["store_nbr","date"]),
            x="date",y="transactions",
            color='store_nbr',title="Transactions")
    save_plot(save_dir, line, "line_chart.html")


    # box chart
    a = transactions.copy()
    a['year'] = a.date.dt.year
    a['month'] = a.date.dt.month
    box = px.box(a, x="year", y="transactions", 
                 color="month",title="Transactions by Year and Month",)
    save_plot(save_dir, box, "box_chart.html")


    # Monthly average transactions line chart
    b = transactions.set_index("date").resample("M").mean().reset_index()
    b["year"] = b.date.dt.year
    monthly_line = px.line(b, x="date", y="transactions", 
                           color = "year", title = "Monthly Average Transactions")
    save_plot(save_dir, monthly_line, "monthly_line_chart.html")


    # scatter chart
    scatter = px.scatter(temp, x="transactions", y="sales",
                         trendline='ols', trendline_color_override='red',
                         title="Scatter Plot of Total Sales vs Transactions")
    save_plot(save_dir, scatter, "scatter_chart.html")

    
    # Weekly average transactions line chart
    c = transactions.copy()
    c["year"] = c.date.dt.year
    c["dayofweek"] = c.date.dt.dayofweek + 1
    c = c.groupby(["year", "dayofweek"]).transactions.mean().reset_index()
    weekly_line = px.line(c, x="dayofweek", y="transactions",
                          color="year", title="Weekly Average Transactions")
 
    save_plot(save_dir, weekly_line, "weekly_line_chart.html")  



    return line, box, monthly_line, scatter









