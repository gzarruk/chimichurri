from chimi import Strategy


class TestStrategy:
    def test_init_works(self) -> None:
        _ = Strategy()
        assert _.pair == "XAU_USD"
        # Make sure the default is the practice account, for security reasons.
        assert not _.live
        assert _.oanda.account_type == "practice"

    def test_get_data(self) -> None:
        """
        Test that retrieving 1 month of daily GOLD price data for January 2023 returns exactly
        22 data points. The OANDA API function for fetching historical data doesn't include the data
        point corresponding to end date, therefore the end dat must be 1st of February to include the 31 of Jan
        data point.
        :return: None
        """
        _ = Strategy(
            start="2023-01-01",
            end="2023-02-01",
            granularity="D",
            price="B",
        ).get_data()
        assert len(_) == 22
