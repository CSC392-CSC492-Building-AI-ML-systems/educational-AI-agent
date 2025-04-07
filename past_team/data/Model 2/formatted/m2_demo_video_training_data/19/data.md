# Asciinema Recording Documentation: Installing and Using `curl` and `vim` on Fedora 38

This documentation outlines a session where the user installs `curl` and `vim` on a Fedora 38 virtual machine, verifies their installations, and uses `curl` to fetch HTTP headers from a webpage.

## Steps in the Recording

1. **Connect to Fedora VM via SSH**  
   Command: `ssh user@fedora-vm`  
   Output:  Welcome to Fedora 38 (Workstation Edition)
- The user connects to the Fedora 38 virtual machine via SSH.

2. **Check the System's Hostname and Details**  
Command: `hostnamectl`  
Output:  Static hostname: fedora-vm Icon name: computer-vm Chassis: vm Machine ID: 1234567890abcdef1234567890abcdef Boot ID: abcdefgh-ijkl-mnop-qrst-uvwxyzabcdef Operating System: Fedora 38 (Workstation Edition) Kernel: Linux 6.0.5-200.fc38.x86_64 Architecture: x86-64
- The user checks the system's hostname, operating system, and kernel details using `hostnamectl`.

3. **Update the Package Index**  
Command: `sudo dnf update -y`  
Output:  Last metadata expiration check: 1:23:45 ago on Wed Nov 15 12:34:56 2024. Dependencies resolved. Nothing to do. Complete!
- The user updates the package index using `dnf update`, but no new updates are available.

4. **Install `curl`**  
Command: `sudo dnf install -y curl`  
Output:  Dependencies resolved.
Package Arch Version Repository Size
Installing: curl x86_64 7.80.0-1.fc38 fedora 736 k
- The user installs `curl` to fetch data from the web.

5. **Verify `curl` by Fetching HTTP Headers**  
Command: `curl -I https://www.example.com`  
Output:  HTTP/1.1 200 OK Date: Wed, 15 Nov 2024 12:35:00 GMT Server: Apache/2.4.48 (Ubuntu) Content-Type: text/html; charset=UTF-8
- The user successfully uses `curl` to fetch the HTTP headers from the webpage `www.example.com`.

6. **Install `vim`**  
Command: `sudo dnf install -y vim`  
Output:  Dependencies resolved.
Package Arch Version Repository Size
Installing: vim x86_64 8.2.2950-1.fc38 fedora 4.8 MB
- The user installs the `vim` text editor on the system.

7. **Verify the Installation of `vim`**  
Command: `vim --version`  
Output:  VIM - Vi IMproved 8.2 (2019 Dec 12, compiled Nov 1 2024 03:22:30) Included patches: 1-1000
- The user verifies the installation of `vim` by checking its version.

8. **Exit the SSH Session**  
Command: `exit`  
Output: None  
- The user exits the SSH session after completing the tasks.

---

## Summary of Commands

| Command                                | Description                                                                      |
|----------------------------------------|----------------------------------------------------------------------------------|
| `ssh user@fedora-vm`                   | Connect to the Fedora virtual machine via SSH.                                   |
| `hostnamectl`                          | Check the system's hostname and details.                                         |
| `sudo dnf update -y`                   | Update the package index using `dnf update`.                                     |
| `sudo dnf install -y curl`             | Install `curl` to fetch data from the web.                                       |
| `curl -I https://www.example.com`      | Fetch HTTP headers from a webpage using `curl`.                                  |
| `sudo dnf install -y vim`              | Install the `vim` text editor on the system.                                     |
| `vim --version`                        | Verify the installation of `vim` by checking its version.                        |
| `exit`                                 | Exit the SSH session.                                                            |
