from ibapi.client import EClient
from ibapi.common import BarData
from ibapi.contract import Contract
from ibapi.wrapper import EWrapper

REQUEST_ID = 1


def create_stock_contract() -> Contract:
    """Create the stock contract used by the historical-data request."""
    contract = Contract()
    contract.symbol = "NVDA"
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.primaryExchange = "NASDAQ"
    return contract


class HistoricalBarsApp(EWrapper, EClient):
    """Request one month of daily historical bars for NVDA."""

    def __init__(self) -> None:
        EClient.__init__(self, wrapper=self)

    def nextValidId(self, orderId: int) -> None:
        """Request historical bars once the API connection is ready."""
        print(f"Connected. Next valid order ID: {orderId}")

        self.reqHistoricalData(
            reqId=REQUEST_ID,
            contract=create_stock_contract(),
            endDateTime="",
            durationStr="1 M",
            barSizeSetting="1 day",
            whatToShow="TRADES",
            useRTH=1,
            formatDate=1,
            keepUpToDate=False,
            chartOptions=[],
        )

    def historicalData(self, reqId: int, bar: BarData) -> None:
        """Print one historical bar returned for the request."""
        print(
            f"{reqId}  {bar.date}  "
            f"O={bar.open} H={bar.high} L={bar.low} C={bar.close} V={bar.volume}"
        )

    def historicalDataEnd(self, reqId: int, start: str, end: str) -> None:
        """Disconnect once all bars for the request have arrived."""
        print(f"Historical request {reqId} complete: {start} -> {end}")
        self.disconnect()


def main() -> None:
    app = HistoricalBarsApp()
    app.connect(host="127.0.0.1", port=7497, clientId=1)
    app.run()


if __name__ == "__main__":
    main()
