# main.py
from gui.app import SyncBridgeApp


def main() -> None:
    """Start the SyncBridge application."""
    app = SyncBridgeApp()
    app.mainloop()


if __name__ == "__main__":
    main()