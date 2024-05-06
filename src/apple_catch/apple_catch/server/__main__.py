from pathlib import Path

from loglad import LoggerBuilder

from .server import Server
from .address import Address

def main():
    config_path = Path("../config/logger_config.yaml")
    builder = LoggerBuilder("main")
    logger = builder.from_yaml(config_path)
    
    server = Server(
        address=Address.from_dynamic_ipv4(port=5050),
        logger=logger)
    server.start()

if __name__ == "__main__":
    main()