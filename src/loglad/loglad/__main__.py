from pathlib import Path
from .logger_builder import LoggerBuilder


def main():
    config_path = Path("./yaml_configs/example_config.yaml")
    builder = LoggerBuilder("main")
    logger = builder.from_yaml(config_path)

    logger.debug("Working!")


if __name__ == "__main__":
    main()