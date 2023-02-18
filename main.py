from chimi import Strategy
from datetime import datetime


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    tauro = Strategy(
        pair="XAU_USD",
        start="2020-01-01",
        end=datetime.now().strftime("%Y-%m-%d"),
        granularity="D",
        price="B",
    )

    data = tauro.get_data()
