
import socket
import tkinter as tk
import customtkinter as ctk

from network.discovery import SyncBridgeDiscovery


class DevicesPage(ctk.CTkFrame):

    def __init__(self, master, on_device_selected=None):
        super().__init__(master, fg_color="#FFF9D9")

        self.hostname = socket.gethostname()
        self.discovered_devices = {}
        self.device_cards = {}
        self.discovery = None
        self.page_active = True

        # Selected destination device
        self.selected_device = None
        self.on_device_selected = on_device_selected

        # =====================================
        # TITLE
        # =====================================

        ctk.CTkLabel(
            self,
            text="Devices",
            font=("Segoe UI", 30, "bold"),
            text_color="#2E8B57"
        ).pack(pady=(25, 5))

        ctk.CTkLabel(
            self,
            text="Manage nearby SyncBridge devices.",
            font=("Segoe UI", 15),
            text_color="gray40"
        ).pack(pady=(0, 20))

        # =====================================
        # MY DEVICE
        # =====================================

        my_device = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=15
        )
        my_device.pack(fill="x", padx=25, pady=(0, 20))

        ctk.CTkLabel(
            my_device,
            text="🖥 My Device",
            font=("Segoe UI", 20, "bold"),
            text_color="#2E8B57"
        ).pack(anchor="w", padx=20, pady=(15, 10))

        ctk.CTkLabel(
            my_device,
            text=f"Name : {self.hostname}",
            font=("Segoe UI", 14)
        ).pack(anchor="w", padx=20)

        ctk.CTkLabel(
            my_device,
            text="Status : Online",
            text_color="#2E8B57",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", padx=20, pady=(0, 15))

        # =====================================
        # NEARBY DEVICES
        # =====================================

        nearby = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=15
        )
        nearby.pack(fill="both", expand=True, padx=25, pady=(0, 20))

        header = ctk.CTkFrame(
            nearby,
            fg_color="transparent"
        )
        header.pack(fill="x", padx=15, pady=(15, 10))

        ctk.CTkLabel(
            header,
            text="Nearby Devices",
            font=("Segoe UI", 20, "bold"),
            text_color="#2E8B57"
        ).pack(side="left")

        self.refresh_button = ctk.CTkButton(
            header,
            text="Refresh",
            width=100,
            fg_color="#2E8B57",
            hover_color="#246B45",
            command=self.refresh_devices
        )
        self.refresh_button.pack(side="right")

        self.status_label = ctk.CTkLabel(
            nearby,
            text="Searching for SyncBridge devices...",
            font=("Segoe UI", 12),
            text_color="#2E8B57"
        )
        self.status_label.pack(anchor="w", padx=18, pady=(0, 8))

        self.device_list = ctk.CTkScrollableFrame(
            nearby,
            fg_color="#F8F8F8"
        )
        self.device_list.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        self.show_empty_message()

        # Start automatic discovery
        self.start_discovery()

    # =====================================
    # START DISCOVERY
    # =====================================

    def start_discovery(self):

        try:
            self.discovery = SyncBridgeDiscovery(
                device_name=self.hostname,
                on_found=self.handle_device_found,
                on_lost=self.handle_device_lost
            )

            self.discovery.start()

            self.status_label.configure(
                text="● Device discovery active",
                text_color="#2E8B57"
            )

        except Exception as error:

            self.discovery = None

            self.status_label.configure(
                text="● Discovery could not start",
                text_color="#C0392B"
            )

            print("Discovery error:", error)

    # =====================================
    # DEVICE FOUND
    # =====================================

    def handle_device_found(self, device):

        if not self.page_active:
            return

        try:
            self.after(
                0,
                lambda d=device: self.add_device(d)
            )
        except tk.TclError:
            pass

    # =====================================
    # DEVICE LOST
    # =====================================

    def handle_device_lost(self, service_name):

        if not self.page_active:
            return

        try:
            self.after(
                0,
                lambda: self.remove_device(service_name)
            )
        except tk.TclError:
            pass

    # =====================================
    # ADD DEVICE
    # =====================================

    def add_device(self, device):

        if not self.page_active:
            return

        service_name = device["service"]

        self.discovered_devices[service_name] = device

        if service_name in self.device_cards:
            return

        if self.empty_label.winfo_exists():
            self.empty_label.destroy()

        card = ctk.CTkFrame(
            self.device_list,
            fg_color="white",
            corner_radius=12
        )
        card.pack(fill="x", pady=8)

        left = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )
        left.pack(side="left", padx=15, pady=10)

        ctk.CTkLabel(
            left,
            text=device["name"],
            font=("Segoe UI", 17, "bold"),
            text_color="#2E8B57"
        ).pack(anchor="w")

        ctk.CTkLabel(
            left,
            text="● Online",
            text_color="#2E8B57",
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w")

        connect_button = ctk.CTkButton(
            card,
            text="Connect",
            width=120,
            fg_color="#2E8B57",
            hover_color="#246B45",
            command=lambda d=device: self.connect_device(d)
        )
        connect_button.pack(side="right", padx=15)

        self.device_cards[service_name] = card
        self.update_device_count()

    # =====================================
    # REMOVE DEVICE
    # =====================================

    def remove_device(self, service_name):

        if not self.page_active:
            return

        self.discovered_devices.pop(service_name, None)

        card = self.device_cards.pop(service_name, None)

        if card:
            card.destroy()

        # Clear selection if the selected device disappears
        if (
            self.selected_device is not None
            and self.selected_device.get("service") == service_name
        ):
            self.selected_device = None

            if self.on_device_selected:
                self.on_device_selected(None)

        self.update_device_count()

        if not self.discovered_devices:
            self.show_empty_message()

    # =====================================
    # EMPTY MESSAGE
    # =====================================

    def show_empty_message(self):

        self.empty_label = ctk.CTkLabel(
            self.device_list,
            text="No SyncBridge devices found.\n"
                 "Waiting for other computers on your local network.",
            font=("Segoe UI", 14),
            text_color="gray50",
            justify="center"
        )
        self.empty_label.pack(pady=40)

    # =====================================
    # DEVICE COUNT
    # =====================================

    def update_device_count(self):

        count = len(self.discovered_devices)

        if self.selected_device:
            self.status_label.configure(
                text=f"● {count} device(s) found | "
                     f"Selected: {self.selected_device['name']}"
            )
        else:
            self.status_label.configure(
                text=f"● Discovery active | {count} device(s) found"
            )

    # =====================================
    # CONNECT / SELECT DEVICE
    # =====================================

    def connect_device(self, device):

        service_name = device.get("service")

        # Confirm the device is still discovered
        if service_name not in self.discovered_devices:
            self.status_label.configure(
                text="Device is no longer available.",
                text_color="#C0392B"
            )
            return

        self.selected_device = self.discovered_devices[service_name]

        print(
            f"Selected device: {self.selected_device['name']}"
        )

        self.status_label.configure(
            text=f"● Selected: {self.selected_device['name']}",
            text_color="#2E8B57"
        )

        # Pass selected device to the parent application
        if self.on_device_selected:
            self.on_device_selected(self.selected_device)

    # =====================================
    # REFRESH
    # =====================================

    def refresh_devices(self):

        if not self.page_active:
            return

        self.refresh_button.configure(state="disabled")

        self.stop_discovery()

        self.discovered_devices.clear()
        self.device_cards.clear()
        self.selected_device = None

        if self.on_device_selected:
            self.on_device_selected(None)

        for widget in self.device_list.winfo_children():
            widget.destroy()

        self.show_empty_message()

        self.status_label.configure(
            text="Refreshing device discovery..."
        )

        self.start_discovery()

        self.refresh_button.configure(state="normal")

    # =====================================
    # STOP DISCOVERY
    # =====================================

    def stop_discovery(self):

        if self.discovery is not None:
            self.discovery.stop()
            self.discovery = None

    # =====================================
    # CLEANUP
    # =====================================

    def destroy(self):

        self.page_active = False
        self.stop_discovery()

        super().destroy()
