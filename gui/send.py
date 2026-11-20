
import os
import threading
import tkinter.filedialog as fd
import customtkinter as ctk

from core.file_sender import send_file as send_file_to_device


class SendPage(ctk.CTkFrame):

    def __init__(self, master, selected_device=None):
        super().__init__(master, fg_color="#FFF9D9")

        self.selected_file = None
        self.selected_device = selected_device
        self.transfer_running = False

        # ==========================
        # TITLE
        # ==========================

        title = ctk.CTkLabel(
            self,
            text="Send File",
            font=("Segoe UI", 30, "bold"),
            text_color="#2E8B57"
        )
        title.pack(pady=(25, 5))

        subtitle = ctk.CTkLabel(
            self,
            text="Choose a file and send it directly to another device.",
            font=("Segoe UI", 15),
            text_color="gray40"
        )
        subtitle.pack(pady=(0, 10))

        self.device_label = ctk.CTkLabel(
            self,
            text=self.get_device_text(),
            font=("Segoe UI", 14, "bold"),
            text_color="#2E8B57"
        )
        self.device_label.pack(pady=(0, 10))

        # ==========================
        # FILE CARD
        # ==========================

        card = ctk.CTkFrame(
            self,
            width=850,
            height=280,
            fg_color="white",
            corner_radius=15
        )
        card.pack(padx=25, pady=20)
        card.pack_propagate(False)

        icon = ctk.CTkLabel(
            card,
            text="📤",
            font=("Segoe UI Emoji", 42)
        )
        icon.pack(pady=(20, 5))

        self.filename = ctk.CTkLabel(
            card,
            text="No file selected",
            font=("Segoe UI", 20, "bold"),
            text_color="#2E8B57"
        )
        self.filename.pack()

        self.fileinfo = ctk.CTkLabel(
            card,
            text="Browse your computer to select a file.",
            font=("Segoe UI", 14),
            text_color="gray45"
        )
        self.fileinfo.pack(pady=(5, 20))

        # ==========================
        # BUTTONS
        # ==========================

        button_frame = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )
        button_frame.pack()

        self.browse_btn = ctk.CTkButton(
            button_frame,
            text="Browse",
            width=180,
            height=42,
            fg_color="#2E8B57",
            hover_color="#246B45",
            command=self.select_file
        )
        self.browse_btn.grid(row=0, column=0, padx=10)

        self.send_btn = ctk.CTkButton(
            button_frame,
            text="Send",
            width=180,
            height=42,
            state="disabled",
            fg_color="#3CB371",
            hover_color="#2E8B57",
            command=self.send_file
        )
        self.send_btn.grid(row=0, column=1, padx=10)

        # ==========================
        # PROGRESS
        # ==========================

        progress_frame = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=15
        )
        progress_frame.pack(fill="x", padx=25, pady=15)

        ctk.CTkLabel(
            progress_frame,
            text="Transfer Progress",
            font=("Segoe UI", 18, "bold"),
            text_color="#2E8B57"
        ).pack(anchor="w", padx=20, pady=(15, 5))

        self.progress = ctk.CTkProgressBar(
            progress_frame,
            width=700,
            progress_color="#2E8B57"
        )
        self.progress.pack(padx=20, pady=5)

        self.progress.set(0)

        self.status = ctk.CTkLabel(
            progress_frame,
            text="Ready",
            font=("Segoe UI", 13),
            text_color="gray40"
        )
        self.status.pack(anchor="w", padx=20, pady=(5, 15))

        self.update_send_button()

    # ======================================================
    # DEVICE INFORMATION
    # ======================================================

    def get_device_text(self):

        if not self.selected_device:
            return "Destination : No device selected"

        return (
            f"Destination : "
            f"{self.selected_device.get('name', 'Unknown device')}"
        )

    def update_send_button(self):

        if (
            self.selected_file
            and self.selected_device
            and not self.transfer_running
        ):
            self.send_btn.configure(state="normal")
        else:
            self.send_btn.configure(state="disabled")

    # ======================================================
    # FILE SELECTION
    # ======================================================

    def select_file(self):

        if self.transfer_running:
            return

        path = fd.askopenfilename()

        if not path:
            return

        self.selected_file = path

        filename = os.path.basename(path)
        filesize = os.path.getsize(path)

        if filesize < 1024:
            size = f"{filesize} Bytes"

        elif filesize < 1024 * 1024:
            size = f"{filesize / 1024:.2f} KB"

        elif filesize < 1024 * 1024 * 1024:
            size = f"{filesize / (1024 * 1024):.2f} MB"

        else:
            size = f"{filesize / (1024 * 1024 * 1024):.2f} GB"

        self.filename.configure(text=filename)

        self.fileinfo.configure(
            text=f"Size : {size}"
        )

        self.progress.set(0)

        self.status.configure(
            text="File selected. Ready to send."
        )

        self.update_send_button()

    # ======================================================
    # START FILE TRANSFER
    # ======================================================

    def send_file(self):

        if self.transfer_running:
            return

        if not self.selected_file:
            return

        if not self.selected_device:
            self.status.configure(
                text="Please select a destination device first."
            )
            return

        receiver_ip = self.selected_device.get("ip")
        receiver_port = self.selected_device.get("port", 5050)

        if not receiver_ip:
            self.status.configure(
                text="Destination IP address is unavailable."
            )
            return

        self.transfer_running = True

        self.progress.set(0)

        self.status.configure(
            text="Connecting to destination device..."
        )

        self.browse_btn.configure(state="disabled")
        self.send_btn.configure(state="disabled")

        thread = threading.Thread(
            target=self.transfer_worker,
            args=(
                self.selected_file,
                receiver_ip,
                receiver_port
            ),
            daemon=True
        )

        thread.start()

    # ======================================================
    # BACKGROUND TRANSFER
    # ======================================================

    def transfer_worker(
        self,
        file_path,
        receiver_ip,
        receiver_port
    ):

        try:

            result = send_file_to_device(
                file_path,
                receiver_ip,
                receiver_port,
                progress_callback=self.report_progress
            )

            self.after(
                0,
                lambda: self.transfer_completed(result)
            )

        except PermissionError:

            self.after(
                0,
                lambda: self.transfer_failed(
                    "Receiver rejected the transfer."
                )
            )

        except Exception as error:

            message = str(error)

            self.after(
                0,
                lambda: self.transfer_failed(message)
            )

    # ======================================================
    # REAL PROGRESS
    # ======================================================

    def report_progress(self, sent, total):

        self.after(
            0,
            lambda: self.update_progress(sent, total)
        )

    def update_progress(self, sent, total):

        if not self.winfo_exists():
            return

        if total > 0:
            percentage = sent / total
            self.progress.set(percentage)

            self.status.configure(
                text=(
                    f"Sending... "
                    f"{percentage * 100:.1f}% "
                    f"({sent:,} / {total:,} bytes)"
                )
            )

    # ======================================================
    # TRANSFER COMPLETED
    # ======================================================

    def transfer_completed(self, result):

        self.transfer_running = False

        self.progress.set(1)

        self.status.configure(
            text=f"Transfer completed: {result['filename']}"
        )

        self.browse_btn.configure(state="normal")

        self.update_send_button()

    
    # TRANSFER FAILED
    

    def transfer_failed(self, message):

        self.transfer_running = False

        self.status.configure(
            text=f"Transfer failed: {message}"
        )

        self.browse_btn.configure(state="normal")

        self.update_send_button()
