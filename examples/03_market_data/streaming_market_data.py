from decimal import Decimal
from threading import Event, Thread
from time import sleep

from ibapi.client import EClient
from ibapi.common import TickAttrib
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum
from ibapi.wrapper import EWrapper

REQUEST_ID = 2
STREAM_SECONDS = 10


def create_stock_contract() -> Contract:
    """Create the stock contract used by the market-data subscription."""
    contract = Contract()
    contract.symbol = "NVDA"
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.primaryExchange = "NASDAQ"
    return contract


class StreamingMarketDataApp(EWrapper, EClient):
    """Subscribe to top-of-book market data for NVDA."""

    def __init__(self) -> None:
        EClient.__init__(self, wrapper=self)
        self.subscription_started = Event()

    def nextValidId(self, orderId: int) -> None:
        """Start the subscription once the API connection is ready."""
        print(f"Connected. Next valid order ID: {orderId}")
        self.reqMktData(
            reqId=REQUEST_ID,
            contract=create_stock_contract(),
            genericTickList="",
            snapshot=False,
            regulatorySnapshot=False,
            mktDataOptions=[],
        )
        self.subscription_started.set()

    def tickPrice(
        self,
        reqId: int,
        tickType: int,
        price: float,
        attrib: TickAttrib,
    ) -> None:
        """Print a price update for the subscription."""
        tick_name = TickTypeEnum.toStr(tickType)
        print(f"PRICE  reqId={reqId}  {tick_name}={price}")

    def tickSize(self, reqId: int, tickType: int, size: Decimal) -> None:
        """Print a size update for the subscription."""
        tick_name = TickTypeEnum.toStr(tickType)
        print(f"SIZE   reqId={reqId}  {tick_name}={size}")


def main() -> None:
    app = StreamingMarketDataApp()
    app.connect(host="127.0.0.1", port=7497, clientId=1)

    api_thread = Thread(target=app.run, name="ibkr-api")
    api_thread.start()

    if not app.subscription_started.wait(timeout=5):
        app.disconnect()
        api_thread.join()
        raise RuntimeError("Market-data subscription did not start")

    sleep(STREAM_SECONDS)

    app.cancelMktData(REQUEST_ID)
    app.disconnect()
    api_thread.join()


if __name__ == "__main__":
    main()
