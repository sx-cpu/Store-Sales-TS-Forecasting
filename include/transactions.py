import pandas as pd
import plotly.express as px
import os


def get_transactions(train, transactions, save_dir="res/transactions"):

    os.makedirs(save_dir, exist_ok=True)

    temp = pd.merge(train.groupby(["date", "store_nbr"]).sales.sum().reset_index(), transactions, how = "left")
    print("Spearman Correlation between Total Sales and Transactions: {:,.4f}".format(
        temp.corr("spearman").sales.loc["transactions"]))
    
    line = px.line(transactions.sort_values(["store_nbr","date"]),
            x="date",y="transactions",
            color='store_nbr',title="Transactions")
    line_path = os.path.join(save_dir, "line_chart.html")
    line.write_html(line_path)
    
    a = transactions.copy()
    a['year'] = a.date.dt.year
    a['month'] = a.date.dt.month
    box = px.box(a, x="year", y="transactions", 
                 color="month",title="Transactions by Year and Month",)
    box_path = os.path.join(save_dir, "box_chart.html")
    box.write_html(box_path)

    print(f"Line chart saved to:{line_path}")
    print(f"Box chart saved to:{box_path}")

    return line, box






