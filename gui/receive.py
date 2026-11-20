
import tkinter.filedialog as fd
import customtkinter as ctk
import time

from pathlib import Path


class ReceivePage(ctk.CTkFrame):

    def __init__(self, master, transfer_manager=None):
        super().__init__(master, fg_color="#FFF9D9")

        self.transfer_manager = transfer_manager
        self.current_sender = "Waiting..."
        self.current_request_id = None
        self.last_layout_width = 0

        # Receiving progress tracking
        self.receive_started_at = None
        self.last_progress_time = None
        self.last_received_bytes = 0
        self.current_file_size = 0

        self.save_location = str(
            Path.home() / "Downloads" / "SyncBridge"
        )

        Path(self.save_location).mkdir(
            parents=True,
            exist_ok=True
        )

        # ==========================================
        # SCROLLABLE CONTENT
        # ==========================================

        self.body = ctk.CTkScrollableFrame(
            self,
            fg_color="#FFF9D9",
            corner_radius=0
        )
        self.body.pack(fill="both", expand=True)

        # ==========================================
        # TITLE
        # ==========================================

        ctk.CTkLabel(
            self.body,
            text="Receive File",
            font=("Segoe UI", 30, "bold"),
            text_color="#2E8B57"
        ).pack(pady=(25, 5))

        ctk.CTkLabel(
            self.body,
            text="Wait for incoming file transfers from nearby devices.",
            font=("Segoe UI", 15),
            text_color="gray40"
        ).pack(pady=(0, 20))

        # ==========================================
        # MAIN CARD
        # ==========================================

        self.card = ctk.CTkFrame(
            self.body,
            fg_color="white",
            corner_radius=15
        )

        self.card.pack(
            fill="x",
            expand=True,
            padx=25,
            pady=20
        )

        ctk.CTkLabel(
            self.card,
            text="📥",
            font=("Segoe UI Emoji", 44)
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            self.card,
            text="Incoming Transfer",
            font=("Segoe UI", 22, "bold"),
            text_color="#2E8B57"
        ).pack()

        self.sender_label = ctk.CTkLabel(
            self.card,
            text="Sender : Waiting...",
            font=("Segoe UI", 14)
        )
        self.sender_label.pack(pady=(18, 5))

        self.filename_label = ctk.CTkLabel(
            self.card,
            text="File : ---",
            font=("Segoe UI", 14),
            wraplength=750
        )
        self.filename_label.pack()

        self.filesize_label = ctk.CTkLabel(
            self.card,
            text="Size : ---",
            font=("Segoe UI", 14)
        )
        self.filesize_label.pack()

        self.speed_label = ctk.CTkLabel(
            self.card,
            text="Speed : ---",
            font=("Segoe UI", 14)
        )
        self.speed_label.pack()

        self.eta_label = ctk.CTkLabel(
            self.card,
            text="ETA : ---",
            font=("Segoe UI", 14)
        )
        self.eta_label.pack()

        # ==========================================
        # ACCEPT / DECLINE BUTTONS
        # ==========================================

        self.button_frame = ctk.CTkFrame(
            self.card,
            fg_color="transparent"
        )
        self.button_frame.pack(pady=10)

        self.accept_btn = ctk.CTkButton(
            self.button_frame,
            text="Accept",
            width=170,
            fg_color="#2E8B57",
            hover_color="#246B45",
            state="disabled",
            command=self.accept_transfer
        )
        self.accept_btn.grid(
            row=0,
            column=0,
            padx=10,
            pady=5
        )

        self.reject_btn = ctk.CTkButton(
            self.button_frame,
            text="Decline",
            width=170,
            fg_color="#C0392B",
            hover_color="#922B21",
            state="disabled",
            command=self.reject_transfer
        )
        self.reject_btn.grid(
            row=0,
            column=1,
            padx=10,
            pady=5
        )

        # ==========================================
        # SAVE LOCATION
        # ==========================================

        self.location_frame = ctk.CTkFrame(
            self.card,
            fg_color="transparent"
        )

        self.location_frame.pack(
            fill="x",
            padx=15,
            pady=(15, 15)
        )

        self.location_label = ctk.CTkLabel(
            self.location_frame,
            text=f"Save To : {self.save_location}",
            width=420,
            anchor="w"
        )

        self.location_label.grid(
            row=0,
            column=0,
            padx=10,
            pady=5,
            sticky="ew"
        )

        self.change_btn = ctk.CTkButton(
            self.location_frame,
            text="Change",
            width=100,
            command=self.choose_location
        )

        self.change_btn.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        self.location_frame.grid_columnconfigure(
            0,
            weight=1
        )

        # ==========================================
        # PROGRESS CARD
        # ==========================================

        self.progress_frame = ctk.CTkFrame(
            self.body,
            fg_color="white",
            corner_radius=15
        )

        self.progress_frame.pack(
            fill="x",
            padx=25,
            pady=15
        )

        ctk.CTkLabel(
            self.progress_frame,
            text="Receive Progress",
            font=("Segoe UI", 18, "bold"),
            text_color="#2E8B57"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        self.progress = ctk.CTkProgressBar(
            self.progress_frame,
            progress_color="#2E8B57"
        )

        self.progress.pack(
            fill="x",
            padx=20,
            pady=5
        )

        self.progress.set(0)

        self.status = ctk.CTkLabel(
            self.progress_frame,
            text="Waiting for incoming connection...",
            font=("Segoe UI", 13),
            text_color="gray40",
            wraplength=750
        )

        self.status.pack(
            anchor="w",
            padx=20,
            pady=(5, 15)
        )

        # ==========================================
        # RESPONSIVE RESIZE
        # ==========================================

        self.bind(
            "<Configure>",
            self.on_resize
        )

        self.after(
            150,
            self.apply_responsive_layout
        )

    # ==========================================
    # RESPONSIVE LAYOUT
    # ==========================================

    def on_resize(self, event):

        if event.widget == self:
            self.apply_responsive_layout(event.width)

    def apply_responsive_layout(self, width=None):

        if width is None:
            width = self.winfo_width()

        if width <= 1 or width == self.last_layout_width:
            return

        self.last_layout_width = width

        narrow = width < 600

        # Accept / Decline buttons
        if narrow:

            self.accept_btn.configure(width=150)
            self.reject_btn.configure(width=150)

            self.accept_btn.grid_configure(
                row=0,
                column=0,
                padx=5
            )

            self.reject_btn.grid_configure(
                row=1,
                column=0,
                padx=5
            )

        else:

            self.accept_btn.configure(width=170)
            self.reject_btn.configure(width=170)

            self.accept_btn.grid_configure(
                row=0,
                column=0,
                padx=10
            )

            self.reject_btn.grid_configure(
                row=0,
                column=1,
                padx=10
            )

        # Save location
        if narrow:

            self.location_label.configure(
                width=max(180, width - 100),
                wraplength=max(150, width - 110)
            )

            self.location_label.grid_configure(
                row=0,
                column=0,
                columnspan=2,
                sticky="ew"
            )

            self.change_btn.grid_configure(
                row=1,
                column=0,
                columnspan=2,
                sticky="e"
            )

        else:

            self.location_label.configure(
                width=420,
                wraplength=750
            )

            self.location_label.grid_configure(
                row=0,
                column=0,
                columnspan=1,
                sticky="ew"
            )

            self.change_btn.grid_configure(
                row=0,
                column=1,
                columnspan=1,
                sticky="e"
            )

        # Text wrapping
        self.filename_label.configure(
            wraplength=max(200, width - 120)
        )

        self.status.configure(
            wraplength=max(200, width - 100)
        )

    # ==========================================
    # SELECT SAVE LOCATION
    # ==========================================

    def choose_location(self):

        folder = fd.askdirectory()

        if not folder:
            return

        self.save_location = folder

        self.location_label.configure(
            text=f"Save To : {folder}"
        )

        if self.transfer_manager:
            self.transfer_manager.receiver.destination = Path(folder)

            self.transfer_manager.receiver.destination.mkdir(
                parents=True,
                exist_ok=True
            )

    # ==========================================
    # INCOMING REQUEST
    # ==========================================

    def incoming_request(
        self,
        sender,
        filename,
        filesize,
        request_id
    ):

        self.current_request_id = request_id
        self.current_sender = sender

        # Reset progress tracking for the new transfer.
        self.receive_started_at = None
        self.last_progress_time = None
        self.last_received_bytes = 0
        self.current_file_size = filesize

        self.sender_label.configure(
            text=f"Sender : {sender}"
        )

        self.filename_label.configure(
            text=f"File : {filename}"
        )

        self.filesize_label.configure(
            text=f"Size : {self.format_size(filesize)}"
        )

        self.speed_label.configure(
            text="Speed : Waiting..."
        )

        self.eta_label.configure(
            text="ETA : Waiting..."
        )

        self.progress.set(0)

        self.accept_btn.configure(state="normal")
        self.reject_btn.configure(state="normal")

        self.status.configure(
            text="Incoming file request. Please respond."
        )

    # ==========================================
    # RECEIVE PROGRESS
    # ==========================================

    @staticmethod
    def format_size(size):

        size = float(size)
        units = ["B", "KB", "MB", "GB", "TB"]

        for unit in units:
            if size < 1024 or unit == "TB":
                return f"{size:.2f} {unit}"

            size /= 1024

        return f"{size:.2f} TB"

    def update_receive_progress(
        self,
        received,
        total,
        filename=None
    ):
        """Display actual incoming file-transfer progress."""

        if total <= 0:
            self.progress.set(1)
            self.speed_label.configure(text="Speed : 0 B/s")
            self.eta_label.configure(text="ETA : 0 seconds")
            self.status.configure(text="File data received. Finalizing...")
            return

        now = time.monotonic()

        if self.receive_started_at is None:
            self.receive_started_at = now
            self.last_progress_time = now
            self.last_received_bytes = 0

        elapsed = now - self.last_progress_time
        bytes_delta = received - self.last_received_bytes

        speed = (
            bytes_delta / elapsed
            if elapsed > 0 and bytes_delta >= 0
            else 0
        )

        self.last_progress_time = now
        self.last_received_bytes = received

        percentage = min(max(received / total, 0), 1)
        self.progress.set(percentage)

        remaining = max(total - received, 0)
        eta = remaining / speed if speed > 0 else 0

        self.speed_label.configure(
            text=f"Speed : {self.format_size(speed)}/s"
        )

        if speed > 0:
            self.eta_label.configure(
                text=f"ETA : {eta:.0f} seconds"
            )
        else:
            self.eta_label.configure(
                text="ETA : Calculating..."
            )

        self.status.configure(
            text=(
                f"Receiving: {self.format_size(received)} / "
                f"{self.format_size(total)} "
                f"({percentage * 100:.1f}%)"
            )
        )

        if received >= total:
            self.status.configure(
                text="All file data received. Finalizing..."
            )

    # ==========================================
    # ACCEPT TRANSFER
    # ==========================================

    def accept_transfer(self):

        if not self.current_request_id:
            return

        if not self.transfer_manager:
            self.status.configure(
                text="Transfer Manager unavailable."
            )
            return

        approved = self.transfer_manager.respond_to_request(
            self.current_request_id,
            True
        )

        if approved:

            self.accept_btn.configure(state="disabled")
            self.reject_btn.configure(state="disabled")

            self.progress.set(0)

            self.status.configure(
                text="Accepted. Waiting for file transfer..."
            )

    # ==========================================
    # REJECT TRANSFER
    # ==========================================

    def reject_transfer(self):

        if not self.current_request_id:
            return

        if not self.transfer_manager:
            return

        rejected = self.transfer_manager.respond_to_request(
            self.current_request_id,
            False
        )

        if rejected:

            self.accept_btn.configure(state="disabled")
            self.reject_btn.configure(state="disabled")

            self.progress.set(0)

            self.status.configure(
                text="Transfer rejected."
            )

            self.current_request_id = None

    # ==========================================
    # RESET PAGE
    # ==========================================

    def reset(self):

        self.current_request_id = None

        self.receive_started_at = None
        self.last_progress_time = None
        self.last_received_bytes = 0
        self.current_file_size = 0

        self.sender_label.configure(
            text="Sender : Waiting..."
        )

        self.filename_label.configure(
            text="File : ---"
        )

        self.filesize_label.configure(
            text="Size : ---"
        )

        self.speed_label.configure(
            text="Speed : ---"
        )

        self.eta_label.configure(
            text="ETA : ---"
        )

        self.progress.set(0)

        self.accept_btn.configure(
            state="disabled"
        )

        self.reject_btn.configure(
            state="disabled"
        )

        self.status.configure(
            text="Waiting for incoming connection..."
        )
