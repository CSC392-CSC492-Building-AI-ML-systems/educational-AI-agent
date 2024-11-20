# Asciinema Recording Documentation: Installing and Using `curl` and `git` on Ubuntu 22.04

This documentation describes a session where the user installs `curl` and `git` on an Ubuntu 22.04 LTS virtual machine, verifies their installations, and makes a web request using `curl`.

## Steps in the Recording

1. **Connect to Ubuntu VM via SSH**  
   Command: `ssh user@ubuntu-vm`  
   Output:  Welcome to Ubuntu 22.04 LTS
- The user connects to the Ubuntu 22.04 virtual machine via SSH.

2. **Check the System's Version and Codename**  
Command: `lsb_release -a`  
Output:  Distributor ID: Ubuntu Description: Ubuntu 22.04 LTS Release: 22.04 Codename: jammy
- The user checks the version and codename of the Ubuntu distribution using `lsb_release`.

3. **Update the Package Index**  
Command: `sudo apt update`  
Output:  Get:1 http://archive.ubuntu.com/ubuntu jammy InRelease [270 kB] ... Fetched 270 kB in 1s (498 kB/s) Reading package lists... Done
- The user updates the package index to ensure the latest packages are available.

4. **Install `curl`**  
Command: `sudo apt install -y curl`  
Output:  Reading package lists... Done Building dependency tree
Reading state information... Done The following additional packages will be installed: ca-certificates
- The user installs `curl` to make web requests from the terminal.

5. **Verify the Installation of `curl`**  
Command: `curl --version`  
Output:  curl 7.81.0 (x86_64-pc-linux-gnu) libcurl/7.81.0 OpenSSL/1.1.1l zlib/1.2.11
- The user verifies the installation of `curl` by checking its version.

6. **Attempt a Web Request with `curl`**  
Command: `curl https://www.example.com`  
Output:  curl: (6) Could not resolve host: www.example.com
- The user encounters a DNS resolution error while attempting a web request using `curl`.

7. **Restart DNS Resolver Service**  
Command: `sudo systemctl restart systemd-resolved`  
Output: None  
- The user restarts the DNS resolver service to fix the DNS issue.

8. **Retry Web Request with `curl`**  
Command: `curl https://www.example.com`  
Output:  <!doctype html> ...
- The user successfully makes a request to the website after restarting the DNS service.

9. **Install `git`**  
Command: `sudo apt install -y git`  
Output:  Reading package lists... Done Building dependency tree
Reading state information... Done The following additional packages will be installed: git-man libc6-dev
- The user installs `git` to manage version control.

10. **Verify the Installation of `git`**  
 Command: `git --version`  
 Output:  
 ```
 git version 2.34.1
 ```
 - The user verifies the installation of `git` by checking its version.

11. **Exit the SSH Session**  
 Command: `exit`  
 Output: None  
 - The user exits the SSH session after completing the tasks.

---

## Summary of Commands

| Command                                | Description                                                                      |
|----------------------------------------|----------------------------------------------------------------------------------|
| `ssh user@ubuntu-vm`                   | Connect to the Ubuntu virtual machine via SSH.                                   |
| `lsb_release -a`                       | Check the version and codename of the Ubuntu distribution.                       |
| `sudo apt update`                      | Update the package index using `apt`.                                            |
| `sudo apt install -y curl`             | Install `curl` to enable web requests from the terminal.                         |
| `curl --version`                       | Verify the installation of `curl` by checking its version.                       |
| `curl https://www.example.com`         | Attempt a web request using `curl`, encountering a DNS error.                    |
| `sudo systemctl restart systemd-resolved` | Restart the DNS resolver service to fix the issue.                               |
| `curl https://www.example.com`         | Successfully make the web request after resolving the DNS issue.                |
| `sudo apt install -y git`              | Install `git` to manage version control.                                         |
| `git --version`                        | Verify the installation of `git` by checking its version.                        |
| `exit`                                 | Exit the SSH session.                                                            |
