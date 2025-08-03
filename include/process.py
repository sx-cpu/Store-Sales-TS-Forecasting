import os


def save_plot(save_dir, plot, filename):

    os.makedirs(save_dir, exist_ok=True)
    filepath = os.path.join(save_dir, filename)
    plot.write_html(filepath)
    print(f"{filename} saved to: {filepath}")
