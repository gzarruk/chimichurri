import streamlit as st
import pandas as pd
import tpqoa
import plotly.io as pio
from PIL import Image
from datetime import datetime

from chimi.viz.candlesticks import get_candlestick_chart

pio.renderers.default = "browser"

# OANDA client setup
api = tpqoa.tpqoa("oanda.cfg")

# Page configuration and parameters
app_title = "Playing Around with Streamlit"
im = Image.open("img/logo.png")
st.set_page_config(page_title=app_title, page_icon=im, layout="wide")
st.title("Strategy Backtesting")

# Available instruments from OANDA
instruments = api.get_instruments()
inst_disp = []
for ind in instruments:
    inst_disp.append(ind[0])


@st.cache(max_entries=10, ttl=3600)
def load_data(
    pair: str = "GBP_JPY",
    start="2020-01-01",
    end=datetime.now().strftime("%Y-%m-%d"),
    granularity="D",
    price="B",
) -> pd.DataFrame:
    df = api.get_history(
        instrument=pair, start=start, end=end, granularity=granularity, price=price
    )
    return df


# Sidebar setup
st.sidebar.markdown("## Strategy Settings")
chosen_instrument = st.sidebar.selectbox("Instrument", inst_disp)


def get_instrument_name_from_selected(choice: str = None, inst: list = None):
    """Get OANDA instrument name for fetching data"""
    name = inst[inst_disp.index(choice)][1]
    return name


inst_name = get_instrument_name_from_selected(chosen_instrument, instruments)
data = load_data(pair=inst_name)

chart = get_candlestick_chart(inst_data=data, name=chosen_instrument)
st.plotly_chart(chart, use_container_width=True)
