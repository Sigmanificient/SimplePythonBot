from app.bot import Bot


def main() -> None:
    """Entry point to load the app."""
    client: Bot = Bot('&')
    client.run()


if __name__ == '__main__':
    main()
