# Asciinema Recording Documentation: Installing and Using `vim`, `pip3`, and Resolving DNS Issues on Ubuntu 22.04

This documentation outlines a session where the user installs `vim` and `pip3` on an Ubuntu 22.04 LTS virtual machine, verifies their installations, and resolves a DNS issue preventing access to a website using `wget`.

## Steps in the Recording

1. **Connect to Ubuntu VM via SSH**  
   Command: `ssh user@ubuntu-vm`  
   Output:  Welcome to Ubuntu 22.04 LTS (Jammy)
- The user connects to the Ubuntu 22.04 LTS virtual machine via SSH.

2. **Check the Disk Space Usage**  
Command: `df -h`  
Output:  Filesystem Size Used Avail Use% Mounted on /dev/sda1 50G 4.0G 43G 9% / tmpfs 4.0G 2.0M 4.0G 1% /dev/shm
- The user checks the disk space usage on the system using `df -h`.

3. **Update the Package Index**  
Command: `sudo apt update`  
Output:  Get:1 http://archive.ubuntu.com/ubuntu jammy InRelease [273 kB] Fetched 273 kB in 1s (380 kB/s) Reading package lists... Done
- The user updates the package lists using `sudo apt update`.

4. **Install `vim`**  
Command: `sudo apt install -y vim`  
Output:  Reading package lists... Done Building dependency tree Reading state information... Done The following additional packages will be installed: vim-common xxd
- The user verifies the installation of `vim` by checking its version.

6. **Install `python3-pip`**  
Command: `sudo apt install -y python3-pip`  
Output:  Reading package lists... Done Building dependency tree Reading state information... Done The following additional packages will be installed: python3-setuptools python3-wheel
- The user installs `python3-pip` to manage Python packages.

7. **Verify `pip3` Installation**  
Command: `pip3 --version`  
Output:  pip 22.3.1 from /usr/lib/python3.10/site-packages/pip (python 3.10)
- The user verifies the installation of `pip3` by checking its version.

8. **Attempt to Fetch a Webpage Using `wget`**  
Command: `wget https://www.example.com`  
Output:  wget: unable to resolve host address 'www.example.com'
- The user attempts to fetch a webpage using `wget` but encounters a DNS resolution issue.

9. **Restart the DNS Resolver Service**  
Command: `sudo systemctl restart systemd-resolved`  
Output: None  
- The user restarts the DNS resolver service to resolve the DNS issue.

10. **Successfully Fetch the Webpage with `wget`**  
 Command: `wget https://www.example.com`  
 Output:  
 ```
 --2024-11-15 13:00:00--  https://www.example.com/
 Resolving www.example.com (www.example.com)... 93.184.216.34, 2001:0db8:85a3:0000:0000:8a2e:0370:7334
 Connecting to www.example.com (www.example.com)|93.184.216.34|:443... connected.
 HTTP request sent, awaiting response... 200 OK
 Length: 1256 (1.2K) [text/html]
 ```
 - The user successfully fetches the webpage using `wget` after restarting the DNS resolver.

11. **Exit the SSH Session**  
 Command: `exit`  
 Output: None  
 - The user exits the SSH session after completing the tasks.

---

## Summary of Commands

| Command                                | Description                                                                      |
|----------------------------------------|----------------------------------------------------------------------------------|
| `ssh user@ubuntu-vm`                   | Connect to the Ubuntu virtual machine via SSH.                                   |
| `df -h`                                | Check the disk space usage on the system.                                        |
| `sudo apt update`                     | Update the package lists using `sudo apt update`.                                |
| `sudo apt install -y vim`              | Install the `vim` text editor on the system.                                     |
| `vim --version`                        | Verify the installation of `vim` by checking its version.                        |
| `sudo apt install -y python3-pip`      | Install `python3-pip` to manage Python packages.                                 |
| `pip3 --version`                       | Verify the installation of `pip3` by checking its version.                       |
| `wget https://www.example.com`         | Attempt to fetch a webpage using `wget`, encountering a DNS issue.              |
| `sudo systemctl restart systemd-resolved` | Restart the DNS resolver service to resolve the DNS issue.                       |
| `wget https://www.example.com`         | Successfully fetch the webpage with `
