
from pathlib import Path
import customtkinter as ctk
from PIL import Image, ImageTk


from gui.dashboard import Dashboard
from core.transfer_manager import TransferManager


class SyncBridgeApp(ctk.CTk):
    """Main SyncBridge application window."""

    WIDTH = 1100
    HEIGHT = 700

    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("SyncBridge v1.0")
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.minsize(900, 600)

        # Set Windows title-bar icon
        icon_path = (
            Path(__file__).resolve().parent.parent
            / "assets"
            / "syncbridge.ico"
        )

        if icon_path.exists():
            self.iconbitmap(str(icon_path))

        # Theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Window close event
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Initialize Transfer Manager
        self.transfer_manager = TransferManager()

        # Start receiving server
        try:
            self.transfer_manager.start()
            print("SyncBridge server started.")

        except OSError as error:
            print(f"Server startup failed: {error}")

        # Dashboard
        self.dashboard = Dashboard(
            self,
            transfer_manager=self.transfer_manager
        )

        self.dashboard.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        # Monitor background networking events
        self.after(100, self.process_transfer_events)

    def process_transfer_events(self):
        """Process networking events safely on the GUI thread."""

        while True:
            event = self.transfer_manager.get_event()

            if event is None:
                break

            event_type = event.get("type")

            if event_type == "server_started":
                print("Receiving server is running.")

            elif event_type == "server_error":
                print(event.get("message"))

            elif event_type == "incoming_request":
                self.dashboard.handle_transfer_event(event)

            elif event_type == "server_stopped":
                print("Receiving server stopped.")

        if self.winfo_exists():
            self.after(100, self.process_transfer_events)

    def on_close(self):
        """Clean up background services before closing."""

        self.transfer_manager.stop()
        self.destroy()
