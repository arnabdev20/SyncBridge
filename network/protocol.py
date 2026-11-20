
import json
import socket
import struct
from pathlib import Path

BUFFER_SIZE = 1024 * 1024
MAX_HEADER_SIZE = 64 * 1024


def receive_exact(sock, size):
    """Receive exactly the requested number of bytes."""

    if not isinstance(size, int) or size < 0:
        raise ValueError("Invalid receive size.")

    data = bytearray()

    while len(data) < size:
        chunk = sock.recv(min(BUFFER_SIZE, size - len(data)))

        if not chunk:
            raise ConnectionError("Connection interrupted.")

        data.extend(chunk)

    return bytes(data)


def send_message(sock, message):
    """Send a JSON message with a length prefix."""

    payload = json.dumps(message).encode("utf-8")

    if len(payload) > MAX_HEADER_SIZE:
        raise ValueError("Message is too large.")

    sock.sendall(struct.pack("!I", len(payload)))
    sock.sendall(payload)


def receive_message(sock):
    """Receive and validate a length-prefixed JSON message."""

    header_length = struct.unpack(
        "!I",
        receive_exact(sock, 4)
    )[0]

    if header_length == 0 or header_length > MAX_HEADER_SIZE:
        raise ValueError("Invalid message header.")

    payload = receive_exact(sock, header_length)

    try:
        message = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("Invalid JSON message.") from error

    if not isinstance(message, dict):
        raise ValueError("Message must be a JSON object.")

    return message


def send_file_data(sock, file_path, progress_callback=None):
    """Transmit a file after receiver approval."""

    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(path)

    file_size = path.stat().st_size

    send_message(sock, {
        "type": "file",
        "filename": path.name,
        "size": file_size
    })

    # Wait for receiver approval.
    sock.settimeout(120)

    try:
        response = receive_message(sock)
    except socket.timeout as error:
        raise TimeoutError(
            "Timed out waiting for receiver approval."
        ) from error

    if response.get("status") != "accepted":
        raise PermissionError("Receiver rejected the file.")

    # Allow the complete file transfer without a short timeout.
    sock.settimeout(None)

    sent = 0

    with path.open("rb") as file:
        while sent < file_size:
            chunk = file.read(min(BUFFER_SIZE, file_size - sent))

            if not chunk:
                raise IOError("Source file changed during transfer.")

            sock.sendall(chunk)
            sent += len(chunk)

            if progress_callback:
                progress_callback(sent, file_size)

    # Wait for receiver confirmation.
    sock.settimeout(120)

    try:
        result = receive_message(sock)
    except socket.timeout as error:
        raise TimeoutError(
            "Timed out waiting for transfer confirmation."
        ) from error

    if result.get("status") != "completed":
        raise IOError(
            result.get(
                "message",
                "Receiver could not complete the transfer."
            )
        )

    return {
        "filename": path.name,
        "size": sent,
        "status": "completed"
    }

