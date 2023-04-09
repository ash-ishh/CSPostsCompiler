import logging

from posts import Platform
from utils import get_checkpoint

logger = logging.getLogger(__name__)


def main():
    checkpoint = get_checkpoint()
    platforms = ['openai', 'deepmind', 'netflix', 'aws-architecture', 'zerodha']
    for platform in platforms:
        try:
            platform_instance = Platform(platform, checkpoint)
            platform_instance.process()
        except Exception as e:
            logger.execption(e)

if __name__ == "__main__":
    main()