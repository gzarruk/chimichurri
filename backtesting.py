import tpqoa
import altair as alt
from chimi.viz import alt_candlesticks
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
    df = api.get_history(
        instrument=pair, start=start, end=end, granularity=granularity, price=price
    )

    df.reset_index(inplace=True)
    df.rename(
        columns={"time": "date", "o": "open", "h": "high", "l": "low", "c": "close"},
        inplace=True,
    )

    chart = alt_candlesticks(source=df)
    chart.show()
