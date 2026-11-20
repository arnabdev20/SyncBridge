
from network.client import SyncBridgeClient


def send_file(
    file_path,
    receiver_ip,
    receiver_port=5050,
    progress_callback=None
):
    """Send a selected file to another SyncBridge device."""

    client = SyncBridgeClient(
        host=receiver_ip,
        port=receiver_port
    )

    client.connect()

    return client.send_file(
        file_path,
        progress_callback=progress_callback
    )
