from json import loads, dumps, decoder
from logging import Logger
from socket import socket, error
from socket import AF_INET, SOCK_STREAM

from .message import Message
from .address import Address

class SimpleMessageProtocol:
    def __init__(self, logger: Logger, message_start: str = "START||", message_end: str = "||END", id: str = "Anonymous"):
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._message_start = message_start
        self._message_end = message_end
        self._logger = logger
        self._id = id   

    def send_string(self, message_str: str):
        message = Message.with_timestamp(sender=self._id, content=message_str)
        self.send_message(message=message)

    def send_message(self, message: Message, destination_socket: socket | None = None):
        json_str_message = dumps(message.to_dict())
        encoded_message = f"{self._message_start}{json_str_message}{self._message_end}".encode()
        socket = destination_socket or self._socket
        self._logger.debug(f"Sending message: '{message.content}'")
        socket.send(encoded_message)

    def recieve_message(self, destination_socket: socket | None = None) -> Message:
        socket = destination_socket or self._socket
        message = ""
        while message.find(self._message_end) == -1:
            message += socket.recv(4).decode()
        
        payload = message.strip().replace(self._message_start, "").replace(self._message_end, "")
        try:
            obj = loads(payload)
        except decoder.JSONDecodeError:
            self._logger.warning(f"JSON decode error for payload: {payload}")
            return Message.failure(self._id)

        return Message.from_dict(obj)

class ClientSimpleMessageProtocol(SimpleMessageProtocol):
    def __init__(self, listener: bool, logger: Logger, message_start: str = "START||", message_end: str = "||END", id: str = "Anonymous"):
        super().__init__(logger, message_start, message_end, id)
        self._listener = listener

    def connect_to_server(self, address: Address) -> str | None:
        self._logger.debug(f"Performing initial SimpleMessageProtocol handshake with server: '{address}'")
        try:
            self._socket.connect(address.tuple)
            self._logger.debug(f"Successfully connected to Server: {address}")
        except:
            self._logger.warning(f"Unable to connect to host {address}")
            return None
        
        message = self.recieve_message()
        self._id = message.content
        self.send_string(self._listener)
        self._logger.debug(f"Initial SimpleMessageProtocol handshake with server '{address}' has completed successfully")
        return self._id

class ServerSimpleMessageProtocol(SimpleMessageProtocol):
    def __init__(self, address: Address, logger: Logger, message_start: str = "START||", message_end: str = "||END", id: str = "Server"):
        super().__init__(logger, message_start, message_end, id)
        self._MAX_CLIENT_QUEUE = 5
        self._address = address
    
    def server_accept(self) -> socket:
        client_socket, client_address = self._socket.accept()
        self._logger.debug(f"Connected to {client_address}")
        return client_socket

    def server_start(self):
        self._server_bind()
        self._server_listen()

    def _server_bind(self):
        try: 
            self._socket.bind(self._address.tuple)
        except error:
            self._logger.exception(f"Unable to bind to socket, with address: {self._address}")
        self._logger.info(f"Successfully bound socket to address: {self._address}")
    
    def _server_listen(self):
        self._socket.listen(self._MAX_CLIENT_QUEUE)
        self._logger.info(f"Now listening on {self._address}")
    
    def on_client_connect(self, client_id: str, client_socket: socket):
        self._logger.debug(f"Performing initial SimpleMessageProtocol handshake with new client: '{client_id}'")
        message = Message.with_timestamp(sender=self._id, content=client_id)
        self.send_message(message=message, destination_socket=client_socket)
        message = self.recieve_message(destination_socket=client_socket)
        self._logger.debug(f"Initial SimpleMessageProtocol handshake with '{client_id}' is now complete.")
        return message.content