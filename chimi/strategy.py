class Strategy:
    def __init__(self, pair: str):
        self.pair = pair


tauro = Strategy("XAU_USD")

print(tauro.pair)
