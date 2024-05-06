from logging import Logger
from socket import AF_INET, SOCK_STREAM
from socket import socket
from pathlib import Path
from _thread import start_new_thread

from loglad import LoggerBuilder

from .ui import client_interface
from .address import Address

class Client:
    def __init__(self, address: Address, logger: Logger) -> None:
        self._logger = logger
        self._address = address
        self._socket = socket(AF_INET, SOCK_STREAM)

    def connect(self):
        try:
            self._socket.connect(self._address.tuple)
            self._logger.debug(f"Successfully connected to Server: {self._address}")
        except:
            self._logger.exception(f"Unable to connect to host {self._address}")

    def listen(self):
        while True:
            message = self._socket.recv(2048).decode().strip()
            self._logger.info(message)

    def send_message(self, message: str):
        try:
            padded_message = message.strip()
            #if len(padded_message) < 2048:
            #    padded_message += " " * (2048 - len(padded_message))
            self._socket.send(padded_message.encode())
        except:
            self._logger.exception(f"Unable to send message '{message}' to server")

def main():
    client_interface()
    config_path = Path("../config/logger_config.yaml")
    builder = LoggerBuilder("main")
    logger = builder.from_yaml(config_path)
    address = Address.from_dynamic_ipv4(5050)
    client = Client(address=address, logger=logger)
    client.connect()
    start_new_thread(client.listen, ())
    while True:
        message = input("Message: ")
        if message.lower() == "exit":
            exit(0)
        client.send_message(message)
        

if __name__ == "__main__":
    main()