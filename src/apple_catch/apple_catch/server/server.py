from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from logging import Logger
from socket import AF_INET, SOCK_STREAM
from socket import socket, error
from _thread import start_new_thread
from typing import Generator

from .address import Address
from .message import Message
from .simple_message_protocol import ServerSimpleMessageProtocol


class Server:
    def __init__(
            self, 
            protocol: ServerSimpleMessageProtocol,
            address: Address,
            logger: Logger):
        self._logger = logger
        self._address = address
        self._protocol = protocol
        self._socket: socket = socket(AF_INET, SOCK_STREAM)
        self._messages: list[Message] = []

    def start(self):
        self._protocol.server_start()
        self._run()

    def get_messages_from_others(self, client_id: str, last_seen_message_dt: datetime) -> Generator[Message, None, None]:
        new_messages = list(filter(lambda m: m.timestamp > last_seen_message_dt and m.sender != client_id, self._messages))
        if len(new_messages) == 0:
            return
        self._logger.debug(f"New Messages for {client_id}: {new_messages}")
        for message in new_messages:
            yield message
            

    def client_connection(self, client_id: str, client_socket: socket):
        listener = self._protocol.on_client_connect(client_id=client_id, client_socket=client_socket)
        last_seen_message_dt = datetime.min
        while True:

            if listener == "True":
                for message in self.get_messages_from_others(client_id, last_seen_message_dt):
                    self._logger.debug(f"Sending message to {client_id}: {message}")
                    self._protocol.send_message(message=message, destination_socket=client_socket)
                    if message.timestamp > last_seen_message_dt:
                        last_seen_message_dt = message.timestamp
            else:
                self._logger.debug(f"Waiting for message from: {client_id}")
                client_message = self._protocol.recieve_message(destination_socket=client_socket)
                self._logger.debug(f"Received message from {client_message.sender}: {client_message.content}")
                self._messages.append(client_message)
            

    def _run(self):
        client_names = ["Bob", "Jeremy", "Anne", "Beatrice"]
        while True:
            client_socket = self._protocol.server_accept()
            start_new_thread(self.client_connection, (client_names.pop(), client_socket))
