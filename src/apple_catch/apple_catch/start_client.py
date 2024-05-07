from socket import AF_INET, SOCK_STREAM
from pathlib import Path

from loglad import LoggerBuilder
import click

from .server import Address, Client, ClientSimpleMessageProtocol
from .entrypoint import entrypoint

@entrypoint.command()
@click.option("--listener", is_flag=True, default=False)
def client(listener: bool):
    config_path = Path("./config/logger_config.yaml")
    builder = LoggerBuilder("main")
    logger = builder.from_yaml(config_path)
    address = Address.from_dynamic_ipv4(5050)
    protocol = ClientSimpleMessageProtocol(listener=listener, logger=logger.getChild("ClientSimpleMessageProtocol"))
    client = Client(address=address, protocol=protocol, logger=logger.getChild("Client"))
    client.connect()
    while True:
        if listener:
            client.listen()
        else:
            message = input("Message: ")
            if message.lower() == "exit":
                exit(0)
            client.send_message(message)