from logging import Logger
from socket import AF_INET, SOCK_STREAM
from socket import socket

from .address import Address
from .simple_message_protocol import SimpleMessageProtocol

class Client:
    def __init__(self, address: Address, protocol: SimpleMessageProtocol, logger: Logger) -> None:
        self._logger = logger
        self._address = address
        self._protocol = protocol
        self._id = "None"

    def connect(self):
        client_id = None
        while client_id is None:
            if (client_id := self._protocol.connect_to_server(self._address)) is not None:
                self._id = client_id
                break
            if input("Try again? y/n: ") == "n":
                self._logger.info("Unable to connect - closing client")
                exit(0)

    def listen(self):
        message = self._protocol.recieve_message()
        self._logger.info(f"Message recieved: {message}")

    def send_message(self, message: str):
        try:
            self._protocol.send_string(message)
        except:
            self._logger.exception(f"Unable to send message '{message}' to server")
