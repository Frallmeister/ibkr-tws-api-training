from decimal import Decimal
from threading import Event, Thread
from time import sleep

from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.wrapper import EWrapper

REQUEST_ID = 3
STREAM_SECONDS = 20


def create_stock_contract() -> Contract:
    """Create the stock contract used by the real-time-bar subscription."""
    contract = Contract()
    contract.symbol = "NVDA"
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.primaryExchange = "NASDAQ"
    return contract


class RealTimeBarsApp(EWrapper, EClient):
    """Subscribe to five-second real-time bars for NVDA."""

    def __init__(self) -> None:
        EClient.__init__(self, wrapper=self)
        self.subscription_started = Event()

    def nextValidId(self, orderId: int) -> None:
        """Start the subscription once the API connection is ready."""
        print(f"Connected. Next valid order ID: {orderId}")
        self.reqRealTimeBars(
            reqId=REQUEST_ID,
            contract=create_stock_contract(),
            barSize=5,
            whatToShow="TRADES",
            useRTH=True,
            realTimeBarsOptions=[],
        )
        self.subscription_started.set()

    def realtimeBar(
        self,
        reqId: int,
        time: int,
        open_: float,
        high: float,
        low: float,
        close: float,
        volume: Decimal,
        wap: Decimal,
        count: int,
    ) -> None:
        """Print one completed five-second bar."""
        print(
            f"BAR reqId={reqId} time={time} "
            f"open={open_} high={high} low={low} close={close} "
            f"volume={volume} wap={wap} count={count}"
        )


def main() -> None:
    app = RealTimeBarsApp()
    app.connect(host="127.0.0.1", port=7497, clientId=1)

    api_thread = Thread(target=app.run, name="ibkr-api")
    api_thread.start()

    if not app.subscription_started.wait(timeout=5):
        app.disconnect()
        api_thread.join()
        raise RuntimeError("Real-time-bar subscription did not start")

    sleep(STREAM_SECONDS)

    app.cancelRealTimeBars(REQUEST_ID)
    app.disconnect()
    api_thread.join()


if __name__ == "__main__":
    main()
