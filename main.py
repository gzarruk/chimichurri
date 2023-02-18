from datetime import datetime

import matplotlib as mpl

from chimi import Strategy

mpl.use("WebAgg")

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    tauro = Strategy(
        pair="XAU_USD",
        start="2020-01-01",
        end=datetime.now().strftime("%Y-%m-%d"),
        granularity="D",
        price="B",
    )

    tauro.get_data()
    fig, ax = tauro.plot()
