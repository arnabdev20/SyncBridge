
import queue
import threading
import uuid

from core.file_receiver import SyncBridgeFileReceiver
from network.server import SyncBridgeServer


class TransferManager:
    """Coordinates incoming file transfers for SyncBridge."""

    def __init__(self, save_directory=None):
        self.events = queue.Queue()

        self.pending_requests = {}
        self.request_lock = threading.Lock()

        self.running = False

        # File receiver
        self.receiver = SyncBridgeFileReceiver(
            destination=save_directory,
            on_file_offer=self.request_approval,
            on_progress=self.report_receive_progress
        )

        # TCP server
        self.server = SyncBridgeServer(
            on_connection=self.receiver.handle_connection
        )

    def start(self):
        """Start the receiving server."""

        if self.running:
            return

        try:
            self.server.start()
            self.running = True

            self.events.put({
                "type": "server_started"
            })

        except OSError as error:
            self.events.put({
                "type": "server_error",
                "message": str(error)
            })

            raise

    def request_approval(self, metadata, address):
        """
        Called by the receiver's networking thread.

        Waits for the user to accept or reject
        the incoming file.
        """

        request_id = str(uuid.uuid4())
        decision_event = threading.Event()

        request = {
            "request_id": request_id,
            "metadata": metadata,
            "sender": metadata.get(
                "sender_name",
                "Unknown device"
            ),
            "decision": None,
            "event": decision_event
        }

        with self.request_lock:
            self.pending_requests[request_id] = request

        # Notify the GUI through a thread-safe queue.
        self.events.put({
            "type": "incoming_request",
            "request_id": request_id,
            "sender": request["sender"],
            "filename": metadata["filename"],
            "filesize": metadata["size"],
            "address": address
        })

        # Wait for the GUI's decision.
        approved = decision_event.wait(timeout=120)

        with self.request_lock:
            self.pending_requests.pop(request_id, None)

        if not approved:
            return False

        return request["decision"] is True

    def respond_to_request(self, request_id, accepted):
        """Called by the GUI when the user accepts or rejects."""

        with self.request_lock:
            request = self.pending_requests.get(request_id)

            if request is None:
                return False

            request["decision"] = bool(accepted)
            request["event"].set()

        return True

    def report_receive_progress(
        self,
        received,
        total,
        filename,
        address
    ):
        """Send real receiving progress to the GUI."""

        self.events.put({
            "type": "receive_progress",
            "received": received,
            "total": total,
            "filename": filename,
            "address": address
        })

    def get_event(self):
        """Get the next event without blocking the GUI."""

        try:
            return self.events.get_nowait()

        except queue.Empty:
            return None

    def stop(self):
        """Stop the receiving server."""

        if not self.running:
            return

        self.running = False

        # Reject any requests still waiting for approval.
        with self.request_lock:
            for request in self.pending_requests.values():
                request["decision"] = False
                request["event"].set()

        self.server.stop()

        self.events.put({
            "type": "server_stopped"
        })
