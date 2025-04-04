# Asciinema Recording Summary: Network Configuration and Troubleshooting

## Connecting to the Remote Server
- **Command:** `ssh user@remote-server.com`
- **Output:** `Welcome to remote server!`
- **Explanation:** The user connects to the remote server via SSH.

## Checking Network Connectivity
- **Command:** `ping 8.8.8.8`
- **Output:** `PING 8.8.8.8 (8.8.8.8): 56 data bytes 64 bytes from 8.8.8.8: icmp_seq=0 ttl=56 time=14.2 ms`
- **Explanation:** The user checks network connectivity by pinging Google's DNS server (8.8.8.8) to ensure the system has internet access.

## Displaying Network Configuration
- **Command:** `ifconfig`
- **Output:** `eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST> mtu 1500 inet 192.168.1.10 netmask 255.255.255.0 broadcast 192.168.1.255`
- **Explanation:** The user displays the network configuration of the server’s primary network interface (`eth0`), showing the assigned IP address and network details.

## Disabling the Network Interface
- **Command:** `sudo ip link set eth0 down`
- **Output:** *(none)*
- **Explanation:** The user temporarily disables the `eth0` network interface.

## Re-enabling the Network Interface
- **Command:** `sudo ip link set eth0 up`
- **Output:** *(none)*
- **Explanation:** The user re-enables the `eth0` network interface after it was temporarily disabled.

## Listing Active Listening Ports
- **Command:** `netstat -tuln`
- **Output:** `Active Internet connections (only servers) Proto Recv-Q Send-Q Local Address Foreign Address State tcp 0 0 0.0.0.0:22 0.0.0.0:* LISTEN`
- **Explanation:** The user lists all active listening ports on the system to check for open services (in this case, SSH is listening on port 22).

## Testing HTTP Connectivity
- **Command:** `curl http://example.com`
- **Output:** `curl: (6) Could not resolve host: example.com`
- **Explanation:** The user attempts to test HTTP connectivity to `example.com`, but the command fails due to DNS resolution issues.

## Restarting Networking Service
- **Command:** `sudo systemctl restart networking`
- **Output:** *(none)*
- **Explanation:** The user restarts the networking service to apply configuration changes and resolve the DNS issue.

## Re-checking Network Connectivity
- **Command:** `ping 8.8.8.8`
- **Output:** `PING 8.8.8.8 (8.8.8.8): 56 data bytes 64 bytes from 8.8.8.8: icmp_seq=0 ttl=56 time=12.3 ms`
- **Explanation:** The user re-runs the `ping` test to verify that network connectivity is restored after restarting the networking service.

## Ending the Session
- **Command:** `exit`
- **Output:** *(none)*
- **Explanation:** The user terminates the Asciinema recording.