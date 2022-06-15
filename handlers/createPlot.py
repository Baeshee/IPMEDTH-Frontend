import matplotlib

matplotlib.use("Qt5Agg")
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from handlers.modelHandler import PandasModel


def createPlot(data):
    colors = ["#ffe5b4", "#804080", "#ffcc00", "#30ff30", "#1565c0", "#ff3030"]
    finger_thumb = pd.DataFrame(data["finger_thumb"])
    finger_index = pd.DataFrame(data["finger_index"])
    finger_middle = pd.DataFrame(data["finger_middle"])
    finger_ring = pd.DataFrame(data["finger_ring"])
    finger_pink = pd.DataFrame(data["finger_pink"])
    wrist = pd.DataFrame(data["wrist"])

    df = pd.concat(
        [finger_thumb, finger_index, finger_middle, finger_ring, finger_pink, wrist],
        axis=1,
    )
    model = PandasModel(df)

    # Omklappen zodat de X en Y coordinaten geinterpreteerd worden voor de plot
    df = df.T

    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)

    padding = 50
    ax.axis(
        [
            df["x"].min() - padding,
            df["x"].max() + padding,
            df["y"].min() - padding,
            df["y"].max() + padding,
        ]
    )

    for k, v in df.iterrows():
        if "THUMB" in k:
            ax.scatter(v[0], v[1], color=colors[0])
        if "INDEX" in k:
            ax.scatter(v[0], v[1], color=colors[1])
        if "MIDDLE" in k:
            ax.scatter(v[0], v[1], color=colors[2])
        if "RING" in k:
            ax.scatter(v[0], v[1], color=colors[3])
        if "PINKY" in k:
            ax.scatter(v[0], v[1], color=colors[4])
        if "WRIST" in k:
            ax.scatter(v[0], v[1], color=colors[5])

        # ax.annotate(k, v,
        #             xytext=(-10,-10),
        #             textcoords='offset points',
        #             size=4,
        #             color='darkslategrey')
    ax.invert_yaxis()

    return fig, model
