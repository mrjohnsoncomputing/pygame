from pathlib import Path

from loglad import LoggerBuilder
import click

from .server import Server, Address, ServerSimpleMessageProtocol
from .entrypoint import entrypoint

@entrypoint.command()
def server():
    config_path = Path("./config/logger_config.yaml")
    builder = LoggerBuilder("main")
    logger = builder.from_yaml(config_path)
    address = Address.from_dynamic_ipv4(port=5050)
    protocol = ServerSimpleMessageProtocol(address=address, logger=logger.getChild("ServerSimpleMessageProtocol"))
    server = Server(
        protocol=protocol,
        address=address,
        logger=logger.getChild("Server"))
    server.start()
