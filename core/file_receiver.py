from pathlib import Path
from network.protocol import (
    receive_message,
    receive_exact,
    send_message,
    BUFFER_SIZE
)


class SyncBridgeFileReceiver:

    def __init__(
        self,
        destination=None,
        on_file_offer=None,
        on_progress=None
    ):
        self.destination = Path(
            destination or Path.home() / "Downloads" / "SyncBridge"
        )

        self.on_file_offer = on_file_offer
        self.on_progress = on_progress

        self.destination.mkdir(
            parents=True,
            exist_ok=True
        )

    def handle_connection(self, connection, address):
        """Handle an incoming file transfer."""

        destination = None
        transfer_completed = False

        try:
            metadata = receive_message(connection)

            if not isinstance(metadata, dict):
                raise ValueError("Invalid transfer metadata.")

            if metadata.get("type") != "file":
                raise ValueError("Unsupported transfer type.")

            filename = metadata.get("filename")
            file_size = metadata.get("size")

            if (
                not isinstance(filename, str)
                or not filename
                or len(filename) > 255
                or Path(filename).name != filename
                or filename in {".", ".."}
            ):
                raise ValueError("Invalid filename.")

            if (
                not isinstance(file_size, int)
                or isinstance(file_size, bool)
                or file_size < 0
            ):
                raise ValueError("Invalid file size.")

            # Ask the receiver to approve or reject.
            approved = False

            if self.on_file_offer:
                approved = self.on_file_offer(metadata, address)

            if not approved:
                send_message(connection, {
                    "status": "rejected"
                })
                return

            send_message(connection, {
                "status": "accepted"
            })

            # Generate a unique destination filename.
            counter = 0

            while True:
                if counter == 0:
                    candidate = self.destination / filename
                else:
                    candidate = (
                        self.destination /
                        f"{Path(filename).stem}_{counter}"
                        f"{Path(filename).suffix}"
                    )

                try:
                    file = candidate.open("xb")
                    destination = candidate
                    break

                except FileExistsError:
                    counter += 1

            received = 0

            with file:
                while received < file_size:

                    chunk_size = min(
                        BUFFER_SIZE,
                        file_size - received
                    )

                    chunk = receive_exact(
                        connection,
                        chunk_size
                    )

                    file.write(chunk)
                    received += len(chunk)

                    # Report actual receiving progress.
                    if self.on_progress:
                        try:
                            self.on_progress(
                                received,
                                file_size,
                                destination.name,
                                address
                            )
                        except Exception as error:
                            print(f"Progress callback error: {error}")

            send_message(connection, {
                "status": "completed",
                "filename": destination.name
            })

            transfer_completed = True

            print(f"File received: {destination}")

        except Exception as error:
            print(f"Receive error: {error}")

            try:
                send_message(connection, {
                    "status": "failed"
                })
            except OSError:
                pass

        finally:
            # Remove incomplete files after interrupted transfers.
            if destination is not None and not transfer_completed:
                try:
                    destination.unlink(missing_ok=True)
                    print(
                        f"Incomplete file removed: {destination}"
                    )
                except OSError as error:
                    print(f"Could not remove incomplete file: {error}")

            connection.close()