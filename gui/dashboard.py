"""
SyncBridge
gui/dashboard.py
"""

import customtkinter as ctk

from gui.send import SendPage
from gui.receive import ReceivePage
from gui.transfers import TransfersPage
from gui.devices import DevicesPage
from gui.settings import SettingsPage


class Dashboard(ctk.CTkFrame):

    def __init__(self, master, transfer_manager=None):
        super().__init__(master, fg_color="#FFF9D9")

        self.transfer_manager = transfer_manager
        self.current_page = None

        # Store the selected destination device
        self.selected_device = None

        # Store navigation buttons so their active state can be updated
        self.nav_buttons = {}

        # ===============================
        # GRID
        # ===============================

        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # ===============================
        # HEADER
        # ===============================

        header = ctk.CTkFrame(
            self,
            height=70,
            fg_color="#2E8B57",
            corner_radius=0
        )

        header.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew"
        )

        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)
        header.grid_columnconfigure(2, weight=0)

        header.grid_propagate(False)

        ctk.CTkLabel(
            header,
            text="SyncBridge",
            font=("Segoe UI", 28, "bold"),
            text_color="white"
        ).grid(row=0, column=0, padx=20, sticky="w")

        ctk.CTkLabel(
            header,
            text="Device : PC-01",
            font=("Segoe UI", 14),
            text_color="white"
        ).grid(row=0, column=1, padx=(0, 20), sticky="e")

        ctk.CTkLabel(
            header,
            text="● Connected",
            font=("Segoe UI", 14, "bold"),
            text_color="#90EE90"
        ).grid(row=0, column=2, padx=(0, 20), sticky="e")

        # ===============================
        # SIDEBAR
        # ===============================

        sidebar = ctk.CTkFrame(
            self,
            width=220,
            fg_color="#2E8B57",
            corner_radius=0
        )

        # Sidebar spans both the content and footer rows so the green
        # background reaches the bottom of the application window.
        sidebar.grid(
            row=1,
            column=0,
            rowspan=2,
            sticky="nsew"
        )

        sidebar.grid_propagate(False)

        menu_font = ("Segoe UI", 15)

        def create_nav_button(name, text, command):
            button = ctk.CTkButton(
                sidebar,
                text=text,
                width=180,
                height=45,
                fg_color="transparent",
                hover_color="#246B45",
                anchor="w",
                font=menu_font,
                command=command
            )

            button.pack(pady=5, padx=15)
            self.nav_buttons[name] = button

        create_nav_button(
            "Dashboard",
            "🏠 Dashboard",
            self.show_home
        )

        create_nav_button(
            "Send",
            "📤 Send",
            lambda: self.show_page(SendPage, "Send")
        )

        create_nav_button(
            "Receive",
            "📥 Receive",
            lambda: self.show_page(ReceivePage, "Receive")
        )

        create_nav_button(
            "Transfers",
            "📂 Transfers",
            lambda: self.show_page(TransfersPage, "Transfers")
        )

        create_nav_button(
            "Devices",
            "👥 Devices",
            lambda: self.show_page(DevicesPage, "Devices")
        )

        create_nav_button(
            "Settings",
            "⚙ Settings",
            lambda: self.show_page(SettingsPage, "Settings")
        )

        # ===============================
        # PAGE CONTAINER
        # ===============================

        self.content = ctk.CTkFrame(
            self,
            fg_color="#FFF9D9",
            corner_radius=0
        )

        self.content.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=20,
            pady=20
        )

        # ===============================
        # FOOTER
        # ===============================

        footer = ctk.CTkFrame(
            self,
            height=35,
            fg_color="#FFF9D9",
            corner_radius=0
        )

        # Footer stays in the main content column. The sidebar occupies
        # column 0 independently and continues behind the footer row.
        footer.grid(
            row=2,
            column=1,
            sticky="ew"
        )

        footer.grid_propagate(False)

        ctk.CTkLabel(
            footer,
            text="© 2026 SyncBridge | Secure Peer-to-Peer File Transfer",
            font=("Segoe UI", 11),
            text_color="gray50"
        ).pack(pady=8)

        # Show dashboard home by default
        self.show_home()

    # ==========================================================
    # NAVIGATION ACTIVE STATE
    # ==========================================================

    def set_active_menu(self, selected):
        """Highlight only the currently selected navigation button."""

        for name, button in self.nav_buttons.items():

            if name == selected:
                button.configure(
                    fg_color="#246B45",
                    hover_color="#1F5A3B"
                )

            else:
                button.configure(
                    fg_color="transparent",
                    hover_color="#246B45"
                )

    # ==========================================================
    # SELECTED DEVICE
    # ==========================================================

    def set_selected_device(self, device):
        """Store the device selected from the Devices page."""

        self.selected_device = device

        if device is None:
            print("No destination device selected.")
            return

        print(
            f"Destination selected: {device.get('name')}"
        )

        print(
            f"Destination IP: {device.get('ip')}"
        )

        print(
            f"Destination port: {device.get('port', 5050)}"
        )

    # ==========================================================
    # PAGE SWITCHING
    # ==========================================================

    def show_page(self, page, menu_name=None):

        # Update the selected sidebar item
        if menu_name:
            self.set_active_menu(menu_name)

        # Remove current page
        for widget in self.content.winfo_children():
            widget.destroy()

        # Load selected page
        if page == ReceivePage:

            frame = ReceivePage(
                self.content,
                transfer_manager=self.transfer_manager
            )

        elif page == DevicesPage:

            frame = DevicesPage(
                self.content,
                on_device_selected=self.set_selected_device
            )

        elif page == SendPage:

            frame = SendPage(
                self.content,
                selected_device=self.selected_device
            )

        else:

            frame = page(self.content)

        frame.pack(fill="both", expand=True)

        self.current_page = frame

    # ==========================================================
    # HANDLE NETWORK EVENTS
    # ==========================================================

    def handle_transfer_event(self, event):

        if event.get("type") != "incoming_request":
            return

        # Open Receive page and highlight Receive in the sidebar
        self.show_page(ReceivePage, "Receive")

        # Display incoming file request
        self.current_page.incoming_request(
            sender=event.get("sender", "Unknown device"),
            filename=event.get("filename", "Unknown file"),
            filesize=event.get("filesize", 0),
            request_id=event.get("request_id")
        )

    # ==========================================================
    # HOME PAGE
    # ==========================================================

    def show_home(self):

        # Highlight Dashboard in the sidebar
        self.set_active_menu("Dashboard")

        # Clear page
        for widget in self.content.winfo_children():
            widget.destroy()

        self.current_page = None

        # Welcome Title
        ctk.CTkLabel(
            self.content,
            text="Welcome to SyncBridge",
            font=("Segoe UI", 30, "bold"),
            text_color="#2E8B57"
        ).pack(pady=(60, 10))

        # Subtitle
        ctk.CTkLabel(
            self.content,
            text="Fast • Secure • Peer-to-Peer File Transfer",
            font=("Segoe UI", 16),
            text_color="gray40"
        ).pack()

        # Send Button
        ctk.CTkButton(
            self.content,
            text="📤 Open Send Page",
            width=260,
            height=45,
            fg_color="#2E8B57",
            hover_color="#246B45",
            command=lambda: self.show_page(SendPage, "Send")
        ).pack(pady=(35, 10))

        # Receive Button
        ctk.CTkButton(
            self.content,
            text="📥 Open Receive Page",
            width=260,
            height=45,
            fg_color="#2E8B57",
            hover_color="#246B45",
            command=lambda: self.show_page(ReceivePage, "Receive")
        ).pack(pady=10)

        # Transfers Button
        ctk.CTkButton(
            self.content,
            text="📂 Open Transfer History",
            width=260,
            height=45,
            fg_color="#2E8B57",
            hover_color="#246B45",
            command=lambda: self.show_page(TransfersPage, "Transfers")
        ).pack(pady=10)

        # Devices Button
        ctk.CTkButton(
            self.content,
            text="👥 Open Devices",
            width=260,
            height=45,
            fg_color="#2E8B57",
            hover_color="#246B45",
            command=lambda: self.show_page(DevicesPage, "Devices")
        ).pack(pady=10)
