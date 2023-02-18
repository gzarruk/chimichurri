from chimi import Strategy


class TestStrategy:
    def test_init_works(self) -> None:
        _ = Strategy()
        assert _.pair == "XAU_USD"
        assert not _.live
        assert _.oanda.account_type == "practice"
