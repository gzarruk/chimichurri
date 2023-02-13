import tpqoa
import altair as alt
from vega_datasets import data
from chimi.viz.candlesticks import alt_candlesticks
from datetime import datetime

# Initial setup and api connection
alt.renderers.enable("altair_viewer")
# OANDA client setup
api = tpqoa.tpqoa("oanda.practice.cfg")
pairs = api.get_instruments()

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    # Input parameters
    pair = "GBP_JPY"
    start = "2020-01-01"
    end = datetime.now().strftime("%Y-%m-%d")
    granularity = "D"
    price = "B"

    # Load historical data
    data = api.get_history(
        instrument=pair, start=start, end=end, granularity=granularity, price=price
    )

    chart = alt_candlesticks(source=data)
    chart.show()
