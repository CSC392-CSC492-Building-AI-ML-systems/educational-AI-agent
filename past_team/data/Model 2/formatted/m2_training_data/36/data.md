# Asciinema Recording Documentation: Configuring a Static IP Address

## Overview
This recording demonstrates the process of configuring a static IP address on a Linux machine using netplan.

---

## Timeline Breakdown

### 1. **Editing the Network Configuration File**
- **Command:** `sudo nano /etc/netplan/01-netcfg.yaml`
- **Output:** *(none)*
- **Explanation:** The user opens the netplan configuration file to modify network settings.

### 2. **Applying the Network Configuration**
- **Command:** `sudo netplan apply`
- **Output:** *(none)*
- **Explanation:** The user applies the changes made to the network configuration file.

### 3. **Verifying the IP Configuration**
- **Command:** `ip a`
- **Output:**  `inet 192.168.1.100/24 brd 192.168.1.255 scope global eth0`
- **Explanation:** The user checks the network interfaces to verify that the static IP has been set.

### 4. **Ending the Session**
- **Command:** `exit`
- **Output:** *(none)*
- **Explanation:** The user exits the session after configuring the network.

---

## Key Takeaways
- **Network Configuration:** Demonstrated editing the netplan file to configure a static IP address.
- **Verification:** Used the `ip a` command to confirm that the IP was correctly applied.