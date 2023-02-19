from datetime import datetime
from pathlib import Path
from typing import Optional, Union

import matplotlib.pyplot as plt
import pandas as pd
import tpqoa

DEMO_CONFIG_FILEPATH = Path(__file__).resolve().parent.parent / "oanda.practice.cfg"
LIVE_CONFIG_FILEPATH = Path(__file__).resolve().parent.parent / "oanda.live.cfg"


class Strategy:
    def __init__(
        self,
        live: bool = False,
        pair: str = "XAU_USD",
        start: Optional[Union[datetime, str]] = None,
        end: Optional[Union[datetime, str]] = None,
        granularity: Optional[str] = None,
        price: Optional[str] = None,
    ) -> None:
        self.data = None
        self.pair = pair
        self.live = live
        self.start = start
        self.end = end
        self.granularity = granularity
        self.price = price
        # Connect to OANDA account
        self.oanda = tpqoa.tpqoa(DEMO_CONFIG_FILEPATH)
        if self.live:
            self.oanda = tpqoa.tpqoa(LIVE_CONFIG_FILEPATH)

    def get_data(self) -> pd.DataFrame:
        """Get data from OANDA API
        Wrapper method for the OANDA API
        """
        self.data = self.oanda.get_history(
            instrument=self.pair,
            start=self.start,
            end=self.end,
            granularity=self.granularity,
            price=self.price,
        )

        return self.data

    def plot(self, target: str = "c") -> tuple[plt.figure, plt.axes]:
        """

        :param target: Name of the DataFrame colum to plot
        :return: tuple[fig, ax] with the handles for the figure generated
        """
        fig, ax = plt.subplots(figsize=(25, 12), frameon=False)
        ax.plot(self.data.index, self.data[target], "-o")

        ax.set(
            xlabel="Date & Time",
            ylabel=self.pair[4:],
            title=self.pair,
        )
        ax.grid()
        fig.tight_layout()
        plt.show()
        return fig, ax
