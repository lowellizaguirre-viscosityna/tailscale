"""TailTray executable entry point."""


def main() -> None:
    from .app import TrayApplication

    TrayApplication().run()


if __name__ == "__main__":
    main()
