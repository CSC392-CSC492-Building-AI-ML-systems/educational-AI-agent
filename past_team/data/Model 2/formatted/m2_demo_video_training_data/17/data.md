# Asciinema Recording Documentation: Installing and Using `wget` and `vim` on Ubuntu 22.04

This documentation describes a session where the user installs `wget` and `vim` on an Ubuntu 22.04 LTS virtual machine, verifies their installations, and uses `wget` to download a webpage.

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

4. **Install `wget`**  
Command: `sudo apt install -y wget`  
Output:  Reading package lists... Done Building dependency tree
Reading state information... Done The following additional packages will be installed: ca-certificates
- The user installs `wget` to download files from the internet using the terminal.

5. **Download a Web Page Using `wget`**  
Command: `wget https://www.example.com`  
Output:  --2024-11-14 12:35:45-- https://www.example.com/ Resolving www.example.com (www.example.com)... 93.184.216.34 Connecting to www.example.com (www.example.com)|93.184.216.34|:443... connected. HTTP request sent, awaiting response... 200 OK Length: 1256 (1.2K) [text/html] Saving to: ‘index.html’
- The user successfully downloads the webpage using `wget`.

6. **View the Contents of the Downloaded HTML File**  
Command: `cat index.html`  
Output:  <!doctype html> ...
- The user views the contents of the downloaded HTML file using the `cat` command.

7. **Install `vim`**  
Command: `sudo apt install -y vim`  
Output:  Reading package lists... Done Building dependency tree
Reading state information... Done The following additional packages will be installed: vim-common
- The user installs the `vim` text editor using `apt`.

8. **Verify the Installation of `vim`**  
Command: `vim --version`  
Output:  VIM - Vi IMproved 8.2 (2019 Dec 12, compiled May 1 2024 05:23:00) Included patches: 1-10 ...
- The user verifies the installation of `vim` by checking its version.

9. **Exit the SSH Session**  
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
| `sudo apt install -y wget`             | Install `wget` to download files from the internet.                              |
| `wget https://www.example.com`         | Download a webpage using `wget`.                                                 |
| `cat index.html`                       | View the contents of the downloaded HTML file using `cat`.                       |
| `sudo apt install -y vim`              | Install the `vim` text editor on the system.                                     |
| `vim --version`                        | Verify the installation of `vim` by checking its version.                        |
| `exit`                                 | Exit the SSH session.                                                            |
