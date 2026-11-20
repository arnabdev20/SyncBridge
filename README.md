# SyncBridge

**Fast, Secure, and Privacy-Focused Peer-to-Peer File Transfer**

SyncBridge is a desktop application designed for direct peer-to-peer file transfer over a local network. No cloud storage, no third-party servers—just fast, direct transfers between your devices.

---

## 🚀 Features
*   **Direct P2P Transfer:** Files are sent directly between devices on the same network.
*   **Privacy First:** Your files never leave your local network. No data is stored in the cloud.
*   **Device Discovery:** Automatically finds other SyncBridge devices on the local network (using Zeroconf/mDNS).
*   **Modern UI:** Built with CustomTkinter for a sleek, responsive, dark-mode-friendly interface.
*   **Progress Tracking:** Real-time speed, ETA, and progress bars for incoming and outgoing transfers.
*   **Secure:** Built-in validation prevents directory traversal attacks and handles interrupted transfers cleanly.

## 🛠️ Technology Stack
*   **Python 3.11+**
*   **CustomTkinter** (User Interface)
*   **Zeroconf** (Local Network Device Discovery)
*   **Sockets/Threading** (Fast TCP Data Transfer)

## 📥 Download & Usage
You do not need Python to run SyncBridge. 
1. Go to the **Releases** tab on the right side of this page.
2. Download the latest `SyncBridge.exe`.
3. Run the application on both your PC and your receiving device (ensure both are on the same Wi-Fi or LAN).
4. Go to the **Devices** tab, find your other device, and click **Connect**.
5. Go to the **Send** tab, pick a file, and send!

## ⚠️ Important Network Note
Because SyncBridge uses local network discovery and port `5050` to transfer files:
*   **Windows Firewall:** You must allow Python/SyncBridge through your Windows Firewall when prompted.
*   **Same Network:** Both devices must be on the same Wi-Fi or Local Area Network (LAN).
*   **Wired/Wireless Mix:** Some routers block discovery between wired (LAN) and wireless (Wi-Fi) devices. If your PC doesn't find your laptop, ensure AP Isolation is disabled on your router, or try connecting both devices to the same network type.

## 🗺️ Roadmap (Future Updates)
This project is actively being developed. Planned features for future releases include:
*   [ ] Manual IP connection (to bypass router discovery blocks).
*   [ ] Pause/Resume functionality for large file transfers.
*   [ ] Transfer history persistence (saving past transfers to a local database).
*   [ ] Cross-platform support (macOS and Linux).
*   [ ] End-to-End Encryption (E2EE) for transfers over public networks.

## 📄 License
This project is licensed under the **GNU General Public License v3.0 (GPLv3)**. 
See the `LICENSE` file for more details. You are free to use, modify, and distribute this software, provided that any modifications are also open-source under the same license and credit is given to the original author.

---
**Author:** Arnab Roy Chowdhury