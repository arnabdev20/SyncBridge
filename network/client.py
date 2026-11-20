
import socket

from network.protocol import send_file_data


class SyncBridgeClient:

    def __init__(self, host, port=5050):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        """Connect to another SyncBridge device."""

        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self.socket.settimeout(10)

        try:
            self.socket.connect((self.host, self.port))
            return True

        except OSError:
            self.socket.close()
            self.socket = None
            raise

    def send_file(self, file_path, progress_callback=None):
        """Send a file through the established connection."""

        if self.socket is None:
            raise ConnectionError("Not connected to receiver.")

        try:
            return send_file_data(
                self.socket,
                file_path,
                progress_callback=progress_callback
            )
        finally:
            self.disconnect()

    def disconnect(self):
        """Close the connection."""

        if self.socket:
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass

            self.socket.close()
            self.socket = None
