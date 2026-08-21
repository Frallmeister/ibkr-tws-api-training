from datetime import datetime

from ibapi.client import EClient
from ibapi.wrapper import EWrapper


class CurrentTimeApp(EWrapper, EClient):
    """Minimal TWS API application that requests the IBKR server time."""

    def __init__(self) -> None:
        EClient.__init__(self, wrapper=self)

    def nextValidId(self, orderId: int) -> None:
        """Called when the API connection is ready for requests."""
        print(f"Connected. Next valid order ID: {orderId}")
        self.reqCurrentTime()

    def currentTime(self, time: int) -> None:
        """Handle the server-time response and end the example."""
        server_time = datetime.fromtimestamp(time).astimezone()
        print(f"IBKR server time: {server_time.isoformat()}")
        self.disconnect()


def main() -> None:
    app = CurrentTimeApp()
    app.connect(host="127.0.0.1", port=7497, clientId=1)
    app.run()


if __name__ == "__main__":
    main()
