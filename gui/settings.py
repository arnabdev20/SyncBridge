# settings.py

import os
import tkinter.filedialog as fd
import customtkinter as ctk


class SettingsPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(
            master,
            fg_color="#FFF9D9"
        )

        
        # DEFAULT VALUES
        

        self.device_name = ctk.StringVar(
            value="PC-01"
        )

        self.download_location = ctk.StringVar(
            value=os.path.join(
                os.path.expanduser("~"),
                "Downloads"
            )
        )

        self.appearance_mode = ctk.StringVar(
            value="Light"
        )

        self.notifications_enabled = ctk.BooleanVar(
            value=True
        )

        self.auto_accept = ctk.BooleanVar(
            value=False
        )

        self.start_with_windows = ctk.BooleanVar(
            value=False
        )

        
        # TITLE
        

        title = ctk.CTkLabel(
            self,
            text="Settings",
            font=("Segoe UI", 30, "bold"),
            text_color="#2E8B57"
        )

        title.pack(
            pady=(25, 5)
        )

        subtitle = ctk.CTkLabel(
            self,
            text="Manage your SyncBridge preferences.",
            font=("Segoe UI", 15),
            text_color="gray40"
        )

        subtitle.pack(
            pady=(0, 20)
        )

        
        # SCROLLABLE CONTENT
        

        self.settings_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        self.settings_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )

       
        # DEVICE SETTINGS
        

        self.create_section_title(
            "Device"
        )

        device_card = self.create_card()

        ctk.CTkLabel(
            device_card,
            text="Device Name",
            font=("Segoe UI", 16, "bold"),
            text_color="#2E8B57"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 3)
        )

        ctk.CTkLabel(
            device_card,
            text="Name shown to other SyncBridge devices.",
            font=("Segoe UI", 12),
            text_color="gray45"
        ).pack(
            anchor="w",
            padx=20
        )

        self.device_entry = ctk.CTkEntry(
            device_card,
            width=400,
            height=38,
            textvariable=self.device_name
        )

        self.device_entry.pack(
            anchor="w",
            padx=20,
            pady=(10, 15)
        )

        
        # STORAGE SETTINGS
        

        self.create_section_title(
            "Storage"
        )

        storage_card = self.create_card()

        ctk.CTkLabel(
            storage_card,
            text="Default Download Location",
            font=("Segoe UI", 16, "bold"),
            text_color="#2E8B57"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 3)
        )

        ctk.CTkLabel(
            storage_card,
            text="Files received from other devices will be saved here.",
            font=("Segoe UI", 12),
            text_color="gray45"
        ).pack(
            anchor="w",
            padx=20
        )

        location_frame = ctk.CTkFrame(
            storage_card,
            fg_color="transparent"
        )

        location_frame.pack(
            fill="x",
            padx=20,
            pady=(10, 15)
        )

        self.location_entry = ctk.CTkEntry(
            location_frame,
            textvariable=self.download_location,
            height=38
        )

        self.location_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        ctk.CTkButton(
            location_frame,
            text="Browse",
            width=100,
            height=38,
            fg_color="#2E8B57",
            hover_color="#246B45",
            command=self.choose_download_location
        ).pack(
            side="right"
        )

        
        # APPEARANCE
        

        self.create_section_title(
            "Appearance"
        )

        appearance_card = self.create_card()

        ctk.CTkLabel(
            appearance_card,
            text="Appearance Mode",
            font=("Segoe UI", 16, "bold"),
            text_color="#2E8B57"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 3)
        )

        ctk.CTkLabel(
            appearance_card,
            text="Choose how SyncBridge looks.",
            font=("Segoe UI", 12),
            text_color="gray45"
        ).pack(
            anchor="w",
            padx=20
        )

        self.appearance_menu = ctk.CTkOptionMenu(
            appearance_card,
            values=[
                "Light",
                "Dark",
                "System"
            ],
            variable=self.appearance_mode,
            width=180,
            height=38,
            fg_color="#2E8B57",
            button_color="#246B45",
            button_hover_color="#1F5A3B",
            command=self.change_appearance
        )

        self.appearance_menu.pack(
            anchor="w",
            padx=20,
            pady=(10, 15)
        )

        
        # TRANSFER SETTINGS
        

        self.create_section_title(
            "Transfers"
        )

        transfer_card = self.create_card()

        # Notifications

        self.notifications_switch = ctk.CTkSwitch(
            transfer_card,
            text="Transfer Notifications",
            variable=self.notifications_enabled,
            progress_color="#2E8B57",
            button_color="#2E8B57",
            button_hover_color="#246B45"
        )

        self.notifications_switch.pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        ctk.CTkLabel(
            transfer_card,
            text="Show notifications when transfers start or finish.",
            font=("Segoe UI", 12),
            text_color="gray45"
        ).pack(
            anchor="w",
            padx=50
        )

        # Auto accept

        self.auto_accept_switch = ctk.CTkSwitch(
            transfer_card,
            text="Automatically Accept Transfers",
            variable=self.auto_accept,
            progress_color="#2E8B57",
            button_color="#2E8B57",
            button_hover_color="#246B45"
        )

        self.auto_accept_switch.pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        ctk.CTkLabel(
            transfer_card,
            text="Automatically accept incoming file transfers.",
            font=("Segoe UI", 12),
            text_color="gray45"
        ).pack(
            anchor="w",
            padx=50
        )

        # Start with Windows

        self.start_switch = ctk.CTkSwitch(
            transfer_card,
            text="Start SyncBridge with Windows",
            variable=self.start_with_windows,
            progress_color="#2E8B57",
            button_color="#2E8B57",
            button_hover_color="#246B45"
        )

        self.start_switch.pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        ctk.CTkLabel(
            transfer_card,
            text="Launch SyncBridge automatically when Windows starts.",
            font=("Segoe UI", 12),
            text_color="gray45"
        ).pack(
            anchor="w",
            padx=50,
            pady=(0, 15)
        )

        
        # ABOUT
       

        self.create_section_title(
            "About"
        )

        about_card = self.create_card()

        ctk.CTkLabel(
            about_card,
            text="SyncBridge",
            font=("Segoe UI", 20, "bold"),
            text_color="#2E8B57"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 3)
        )

        ctk.CTkLabel(
            about_card,
            text="Secure Peer-to-Peer File Transfer",
            font=("Segoe UI", 13),
            text_color="gray40"
        ).pack(
            anchor="w",
            padx=20
        )

        ctk.CTkLabel(
            about_card,
            text="Version 1.0",
            font=("Segoe UI", 12),
            text_color="gray50"
        ).pack(
            anchor="w",
            padx=20,
            pady=(3, 15)
        )

        
        # SAVE BUTTON
        

        ctk.CTkButton(
            self,
            text="Save Settings",
            width=200,
            height=42,
            fg_color="#2E8B57",
            hover_color="#246B45",
            command=self.save_settings
        ).pack(
            pady=(0, 20)
        )

    
    # CREATE SECTION TITLE
    

    def create_section_title(self, text):

        ctk.CTkLabel(
            self.settings_frame,
            text=text,
            font=("Segoe UI", 18, "bold"),
            text_color="#2E8B57"
        ).pack(
            anchor="w",
            padx=5,
            pady=(10, 5)
        )

    
    # CREATE CARD
    
    def create_card(self):

        card = ctk.CTkFrame(
            self.settings_frame,
            fg_color="white",
            corner_radius=15
        )

        card.pack(
            fill="x",
            pady=(0, 10)
        )

        return card

    
    # DOWNLOAD LOCATION
    

    def choose_download_location(self):

        folder = fd.askdirectory()

        if not folder:
            return

        self.download_location.set(
            folder
        )

   
    # APPEARANCE
    

    def change_appearance(self, mode):

        ctk.set_appearance_mode(
            mode
        )

    # ==========================================
    # SAVE SETTINGS
    # ==========================================

    def save_settings(self):

        print("Settings saved")

        print(
            "Device Name:",
            self.device_name.get()
        )

        print(
            "Download Location:",
            self.download_location.get()
        )

        print(
            "Appearance:",
            self.appearance_mode.get()
        )

        print(
            "Notifications:",
            self.notifications_enabled.get()
        )

        print(
            "Auto Accept:",
            self.auto_accept.get()
        )

        print(
            "Start with Windows:",
            self.start_with_windows.get()
        )