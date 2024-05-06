from logging import Logger
from socket import AF_INET, SOCK_STREAM
from socket import socket, error

from .address import Address

MAX_CLIENT_QUEUE = 5

class Server:
    def __init__(
            self, 
            address: Address,
            logger: Logger):
        self._logger = logger
        self._address = address
        self._socket: socket = socket(AF_INET, SOCK_STREAM)

    def _bind_socket(self):
        try: 
            self._socket.bind(self._address.tuple)
        except error:
            self._logger.exception(f"Unable to bind to socket, with address: {self._address}")
        self._logger.info(f"Successfully bound socket to address: {self._address}")

    def start(self):
        self._bind_socket()
        self._socket.listen(MAX_CLIENT_QUEUE)
        self._logger.info(f"Now listening on {self._address}")
        self._run()

    def _run(self):
        while True:
            client_socket, client_address = self._socket.accept()
            self._logger.debug(f"Connected to {client_address}")
