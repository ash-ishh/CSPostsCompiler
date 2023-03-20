from posts import Platform
from utils import get_checkpoint


def main():
    checkpoint = get_checkpoint()
    platforms = ['openai', 'deepmind', 'netflix', 'aws-architecture']
    for platform in platforms:
        try:
            platform_instance = Platform(platform, checkpoint)
            platform_instance.process()
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()