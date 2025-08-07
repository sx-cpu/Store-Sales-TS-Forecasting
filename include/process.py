import os


def save_plot(filepath, plot):

    plot.write_html(filepath)
    print(f"The plot has been saved to: {filepath}")


