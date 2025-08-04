import pandas as pd
import plotly.express as px
import os
from include.process import save_plot


class TransactionsProcessor:
    def __init__(self, transactions_df, temp_df, save_dir="res/transactions"):
        self.transactions = transactions_df.copy()
        self.temp = temp_df.copy()
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)

    def process(self):
        # Spearman correlation
        print("Spearman Correlation between Total Sales and Transactions: {:,.4f}".format(
            self.temp.corr("spearman").sales.loc["transactions"]
        ))

        # Line chart
        line_path = os.path.join(self.save_dir, "line_chart.html")
        if not os.path.exists(line_path):
            line = px.line(self.transactions.sort_values(["store_nbr", "date"]),
                           x="date", y="transactions",
                           color='store_nbr', title="Transactions")
            save_plot(line_path, line)
        else:
            print(f"Line chart already exists: {line_path}")

        # Box chart
        box_path = os.path.join(self.save_dir, "box_chart.html")
        if not os.path.exists(box_path):
            a = self.transactions.copy()
            a['year'] = a.date.dt.year
            a['month'] = a.date.dt.month
            box = px.box(a, x="year", y="transactions",
                         color="month", title="Transactions by Year and Month")
            save_plot(box_path, box)
        else:
            print(f"Box chart already exists: {box_path}")

        # Monthly average line chart
        monthly_path = os.path.join(self.save_dir, "monthly_line_chart.html")
        if not os.path.exists(monthly_path):
            b = self.transactions.set_index("date").resample("M").mean().reset_index()
            b["year"] = b.date.dt.year
            monthly_line = px.line(b, x="date", y="transactions",
                                   color="year", title="Monthly Average Transactions")
            save_plot(monthly_path, monthly_line)
        else:
            print(f"Monthly average chart already exists: {monthly_path}")

        # Scatter chart
        scatter_path = os.path.join(self.save_dir, "scatter_chart.html")
        if not os.path.exists(scatter_path):
            scatter = px.scatter(self.temp, x="transactions", y="sales",
                                 trendline='ols', trendline_color_override='red',
                                 title="Scatter Plot of Total Sales vs Transactions")
            save_plot(scatter_path, scatter)
        else:
            print(f"Scatter chart already exists: {scatter_path}")

        # Weekly average transactions line chart
        weekly_path = os.path.join(self.save_dir, "weekly_line_chart.html")
        if not os.path.exists(weekly_path):
            c = self.transactions.copy()
            c["year"] = c.date.dt.year
            c["dayofweek"] = c.date.dt.dayofweek + 1
            c = c.groupby(["year", "dayofweek"]).transactions.mean().reset_index()
            weekly_line = px.line(c, x="dayofweek", y="transactions",
                                  color="year", title="Weekly Average Transactions")
            save_plot(weekly_path, weekly_line)
        else:
            print(f"Weekly chart already exists: {weekly_path}")
