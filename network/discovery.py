
import socket
import uuid
import threading

from zeroconf import Zeroconf, ServiceInfo, ServiceBrowser


SERVICE_TYPE = "_syncbridge._tcp.local."
DEFAULT_PORT = 5050


def get_local_ip():
    """Find the local IPv4 address used by the network interface."""

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.connect(("192.0.2.1", 80))
        return sock.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        sock.close()


class SyncBridgeDiscovery:

    def __init__(
        self,
        device_name=None,
        on_found=None,
        on_lost=None,
        port=DEFAULT_PORT
    ):
        self.device_name = device_name or socket.gethostname()
        self.on_found = on_found
        self.on_lost = on_lost
        self.port = port

        self.device_id = str(uuid.uuid4())

        self.zeroconf = None
        self.browser = None
        self.service_info = None

        self.running = False
        self.lock = threading.Lock()

    def start(self):
        """Advertise this computer and discover other computers."""

        if self.running:
            return

        local_ip = get_local_ip()

        if local_ip == "127.0.0.1":
            raise OSError("Could not determine the local network IP.")

        self.zeroconf = Zeroconf()

        service_name = (
            f"{self.device_name}-{self.device_id[:8]}.{SERVICE_TYPE}"
        )

        self.service_info = ServiceInfo(
            SERVICE_TYPE,
            service_name,
            addresses=[socket.inet_aton(local_ip)],
            port=self.port,
            properties={
                "device_name": self.device_name,
                "device_id": self.device_id
            },
            server=f"{socket.gethostname()}.local."
        )

        try:
            self.zeroconf.register_service(self.service_info)

            self.browser = ServiceBrowser(
                self.zeroconf,
                SERVICE_TYPE,
                listener=self
            )

            self.running = True

            print(
                f"SyncBridge discovery active: "
                f"{self.device_name} ({local_ip})"
            )

        except Exception:
            self.zeroconf.close()
            self.zeroconf = None
            raise

    def add_service(self, zeroconf, service_type, name):
        """Called when another SyncBridge device is discovered."""

        if not self.running:
            return

        try:
            info = zeroconf.get_service_info(
                service_type,
                name,
                timeout=3000
            )

            if info is None:
                return

            properties = info.properties or {}

            device_id = properties.get(
                b"device_id",
                b""
            ).decode("utf-8", errors="replace")

            # Ignore this computer's own advertisement.
            if device_id == self.device_id:
                return

            addresses = info.parsed_addresses()

            if not addresses:
                return

            ip_address = next(
                (
                    address for address in addresses
                    if ":" not in address
                ),
                None
            )

            if not ip_address:
                return

            device_name = properties.get(
                b"device_name",
                b"Unknown device"
            ).decode("utf-8", errors="replace")

            device = {
                "service": name,
                "name": device_name,
                "ip": ip_address,
                "port": info.port,
                "device_id": device_id
            }

            print(
                f"Discovered: {device_name} at "
                f"{ip_address}:{info.port}"
            )

            if self.on_found:
                self.on_found(device)

        except Exception as error:
            print("Discovery error:", error)

    def update_service(self, zeroconf, service_type, name):
        """Refresh a device when its service information changes."""

        self.add_service(zeroconf, service_type, name)

    def remove_service(self, zeroconf, service_type, name):
        """Called when another device disappears."""

        if self.on_lost:
            self.on_lost(name)

    def stop(self):
        """Stop discovery and remove this computer's advertisement."""

        if not self.running:
            return

        self.running = False

        try:
            if self.browser:
                self.browser.cancel()
                self.browser = None

            if self.zeroconf and self.service_info:
                self.zeroconf.unregister_service(
                    self.service_info
                )

        except Exception as error:
            print("Discovery shutdown error:", error)

        finally:
            if self.zeroconf:
                self.zeroconf.close()

            self.zeroconf = None
            self.service_info = None

        print("SyncBridge discovery stopped.")
