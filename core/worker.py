import sys
import asyncio
import logging
import logging.config

from uvicorn.config import LOGGING_CONFIG


from config import Settings
from src.infrastructure.command import WorkerCommand


def configure_logging():
    """Configure logging"""
    logging.config.dictConfig(LOGGING_CONFIG)


async def main():
    """Main function"""
    settings = Settings()
    command = WorkerCommand(settings)
    await command.execute()


if __name__ == '__main__':
    configure_logging()
    logger = logging.getLogger('uvicorn')
    try:
        logger.info('Worker starting')
        asyncio.run(main())

    except KeyboardInterrupt:
        logger.info('Worker stopped')
        sys.exit(0)

    except Exception as e:
        logger.error(f'Worker failed: {e}')
        sys.exit(1)
