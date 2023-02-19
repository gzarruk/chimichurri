import matplotlib as mpl

from chimi import Strategy

mpl.use("WebAgg")

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    tauro = Strategy(
        pair="XAU_USD",
        start="2023-01-01",
        end="2023-01-31",
        granularity="D",
        price="B",
    )

    data = tauro.get_data()

    print(len(data))
    print(data.head())
    print(data.tail())

    fig, ax = tauro.plot()
