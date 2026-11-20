
import socket
import threading

HOST = "0.0.0.0"
PORT = 5050
BUFFER_SIZE = 1024 * 1024


class SyncBridgeServer:

    def __init__(self, on_connection=None):
        self.host = HOST
        self.port = PORT
        self.on_connection = on_connection

        self.server_socket = None
        self.running = False
        self.server_thread = None

    def start(self):
        """Start listening for incoming connections."""

        if self.running:
            return

        self.server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self.server_socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )

        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        self.running = True

        self.server_thread = threading.Thread(
            target=self._listen,
            daemon=True
        )

        self.server_thread.start()

        print(f"SyncBridge server listening on port {self.port}")

    def _listen(self):
        """Accept incoming connections."""

        while self.running:
            try:
                connection, address = self.server_socket.accept()

                print(f"Connection received from {address}")

                client_thread = threading.Thread(
                    target=self._handle_connection,
                    args=(connection, address),
                    daemon=True
                )

                client_thread.start()

            except OSError:
                if self.running:
                    print("Server socket error.")
                break

    def _handle_connection(self, connection, address):
        """Handle an incoming connection."""

        try:
            if self.on_connection:
                self.on_connection(connection, address)
            else:
                connection.close()

        except Exception as error:
            print(f"Connection error: {error}")

            try:
                connection.close()
            except OSError:
                pass

    def stop(self):
        """Stop the server."""

        self.running = False

        if self.server_socket:
            try:
                self.server_socket.close()
            except OSError:
                pass

            self.server_socket = None

        print("SyncBridge server stopped.")
