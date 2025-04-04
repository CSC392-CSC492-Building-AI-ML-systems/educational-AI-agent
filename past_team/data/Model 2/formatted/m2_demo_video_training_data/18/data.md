# Asciinema Recording Documentation: Installing and Using `pip3`, `git`, and Troubleshooting DNS Issues on Debian 11

This documentation outlines a session where the user installs `pip3` and `git` on a Debian 11 virtual machine, verifies their installations, and resolves a DNS issue when trying to access a website using `curl`.

## Steps in the Recording

1. **Connect to Debian VM via SSH**  
   Command: `ssh user@debian-vm`  
   Output:  Welcome to Debian GNU/Linux 11 (bullseye)
- The user connects to the Debian 11 virtual machine via SSH.

2. **Check the System's Uptime**  
Command: `uptime`  
Output:  12:34:56 up 1 day, 3:22, 2 users, load average: 0.12, 0.13, 0.09
- The user checks the system's uptime and load averages using the `uptime` command.

3. **Update the Package Index**  
Command: `sudo apt update`  
Output:  Get:1 http://deb.debian.org/debian bullseye InRelease [116 kB] ... Fetched 116 kB in 1s (210 kB/s) Reading package lists... Done
- The user updates the package index to ensure the latest packages are available.

4. **Install `python3-pip`**  
Command: `sudo apt install -y python3-pip`  
Output:  Reading package lists... Done Building dependency tree Reading state information... Done The following additional packages will be installed: python3-setuptools python3-wheel
- The user installs `python3-pip` to manage Python packages on the system.

5. **Verify the Installation of `pip3`**  
Command: `pip3 --version`  
Output:  pip 22.3.1 from /usr/lib/python3.9/site-packages/pip (python 3.9)
- The user verifies the installation of `pip3` by checking its version.

6. **Install `git`**  
Command: `sudo apt install -y git`  
Output:  Reading package lists... Done Building dependency tree Reading state information... Done The following additional packages will be installed: git-man libc6-dev
- The user installs `git` to manage version control.

7. **Verify the Installation of `git`**  
Command: `git --version`  
Output:  git version 2.30.2
- The user verifies the installation of `git` by checking its version.

8. **Attempt to Access a Website with `curl`**  
Command: `curl https://www.example.com`  
Output:  curl: (6) Could not resolve host: www.example.com
- The user encounters a DNS resolution error while trying to access a website using `curl`.

9. **Restart the DNS Resolver Service**  
Command: `sudo systemctl restart systemd-resolved`  
Output: None  
- The user restarts the DNS resolver service to resolve the DNS issue.

10. **Successfully Access the Website with `curl`**  
 Command: `curl https://www.example.com`  
 Output:  
 ```
 <!doctype html> ...
 ```
 - The user successfully accesses the website using `curl` after restarting the DNS resolver.

11. **Exit the SSH Session**  
 Command: `exit`  
 Output: None  
 - The user exits the SSH session after completing the tasks.

---

## Summary of Commands

| Command                                | Description                                                                      |
|----------------------------------------|----------------------------------------------------------------------------------|
| `ssh user@debian-vm`                   | Connect to the Debian virtual machine via SSH.                                   |
| `uptime`                               | Check the system's uptime and load averages.                                     |
| `sudo apt update`                      | Update the package index using `apt`.                                            |
| `sudo apt install -y python3-pip`      | Install `python3-pip` to manage Python packages.                                 |
| `pip3 --version`                       | Verify the installation of `pip3` by checking its version.                       |
| `sudo apt install -y git`              | Install `git` to manage version control.                                         |
| `git --version`                        | Verify the installation of `git` by checking its version.                        |
| `curl https://www.example.com`         | Attempt to access a website using `curl`, encountering a DNS error.              |
| `sudo systemctl restart systemd-resolved` | Restart the DNS resolver service to resolve the DNS issue.                       |
| `curl https://www.example.com`         | Successfully access the website with `curl` after restarting the DNS service.    |
| `exit`                                 | Exit the SSH session.                                                            |
