
import customtkinter as ctk


class TransfersPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="#FFF9D9")

        title = ctk.CTkLabel(
            self,
            text="Transfer History",
            font=("Segoe UI", 30, "bold"),
            text_color="#2E8B57"
        )
        title.pack(pady=(25, 5))

        subtitle = ctk.CTkLabel(
            self,
            text="View your transfer history.",
            font=("Segoe UI", 15),
            text_color="gray40"
        )
        subtitle.pack(pady=(0, 20))

        self.history = ctk.CTkScrollableFrame(
            self,
            fg_color="white",
            corner_radius=15
        )

        self.history.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.add_demo_data()

    # =====================================

    def add_demo_data(self):

        self.add_card(
            "Movie.mp4",
            "Sent",
            "2.1 GB",
            "Completed",
            "Today 10:25 PM"
        )

        self.add_card(
            "Photo.zip",
            "Received",
            "350 MB",
            "Completed",
            "Today 8:10 PM"
        )

        self.add_card(
            "Music.mp3",
            "Sent",
            "8 MB",
            "Failed",
            "Yesterday"
        )

    # =====================================

    def add_card(
        self,
        filename,
        direction,
        size,
        status,
        date
    ):

        card = ctk.CTkFrame(
            self.history,
            fg_color="#F8F8F8",
            corner_radius=12
        )

        card.pack(
            fill="x",
            padx=10,
            pady=8
        )

        ctk.CTkLabel(
            card,
            text=filename,
            font=("Segoe UI", 18, "bold"),
            text_color="#2E8B57"
        ).pack(anchor="w", padx=15, pady=(12, 2))

        ctk.CTkLabel(
            card,
            text=f"Direction : {direction}",
            font=("Segoe UI", 13)
        ).pack(anchor="w", padx=15)

        ctk.CTkLabel(
            card,
            text=f"Size : {size}",
            font=("Segoe UI", 13)
        ).pack(anchor="w", padx=15)

        ctk.CTkLabel(
            card,
            text=f"Status : {status}",
            font=("Segoe UI", 13)
        ).pack(anchor="w", padx=15)

        ctk.CTkLabel(
            card,
            text=f"Date : {date}",
            font=("Segoe UI", 13)
        ).pack(anchor="w", padx=15, pady=(0, 12))
