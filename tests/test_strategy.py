import pytest
from chimi import Strategy


class TestStrategy:
    def test_init_works(self):
        _ = Strategy()
        assert _.pair == "XAU_USD"
        assert not _.live
        assert _.oanda.account_type == "practice"
