from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from logging import Logger
from socket import AF_INET, SOCK_STREAM
from socket import socket, error
from _thread import start_new_thread
from typing import Generator

from .address import Address

MAX_CLIENT_QUEUE = 5

@dataclass
class Message:
    sender: str
    content: str
    timestamp: datetime

    @classmethod
    def with_timestamp(cls, sender: str, content: str):
        return cls(
            sender=sender,
            content=content,
            timestamp = datetime.now()
        )

    def __str__(self) -> str:
        message = f"{self.sender}: {self.content}"
        #if len(message) < 2048:
        #    message += " " * (2048 - len(message))
        return message

class Server:
    def __init__(
            self, 
            address: Address,
            logger: Logger):
        self._logger = logger
        self._address = address
        self._socket: socket = socket(AF_INET, SOCK_STREAM)
        self._messages: list[Message] = []

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


    def get_messages_from_others(self, client_id: str, last_seen_message_dt: datetime) -> Generator[Message, None, None]:
        new_messages = list(filter(lambda m: m.timestamp > last_seen_message_dt and m.sender != client_id, self._messages))
        self._logger.debug(f"New Messages for {client_id}: {new_messages}")
        for message in new_messages:
            yield message
            

    def client_connection(self, client_id: str, client_socket: socket, client_address):
        welcome_message = f"Hello from the Server! - You have been assigned the unique ID '{client_id}'"
        client_socket.send(welcome_message.encode())

        last_seen_message_dt = datetime.min
        while True:
            for message in self.get_messages_from_others(client_id, last_seen_message_dt):
                self._logger.debug(f"Sending message to {client_id}: {message}")
                client_socket.send(str(message).encode())
                if message.timestamp > last_seen_message_dt:
                    last_seen_message_dt = message.timestamp

            self._logger.debug(f"Waiting for message from: {client_id}")
            client_message = client_socket.recv(2048)
            if client_message:
                decoded_message = client_message.decode().strip()
                self._logger.debug(f"Received message from {client_id}: {decoded_message}")
                self._messages.append(Message.with_timestamp(sender=client_id, content=decoded_message))
            

    def _run(self):
        client_names = ["Bob", "Jeremy", "Anne", "Beatrice"]
        while True:
            client_socket, client_address = self._socket.accept()
            self._logger.debug(f"Connected to {client_address}")
            start_new_thread(self.client_connection, (client_names.pop(), client_socket, client_address))
