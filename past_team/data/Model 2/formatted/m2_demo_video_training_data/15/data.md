# Asciinema Recording Documentation: Installing and Using `git` on Ubuntu 22.04

This documentation describes a session in which the user installs, uses, and removes the `git` version control tool on an Ubuntu 22.04 LTS virtual machine. The session also includes building `git` from the official GitHub repository, verifying installations, and checking package manager outputs.

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

4. **Upgrade Installed Packages**  
Command: `sudo apt upgrade -y`  
Output:  Reading package lists... Done Building dependency tree
Reading state information... Done Calculating upgrade... Done The following packages will be upgraded: libc-bin libc6 libc6-dev 3 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.
- The user upgrades installed packages using `apt upgrade`.

5. **Install `git`**  
Command: `sudo apt install -y git`  
Output:  Reading package lists... Done Building dependency tree
Reading state information... Done The following additional packages will be installed: git-man libc6-dev libcurl4-openssl-dev liberror-perl
- The user installs the `git` package along with necessary dependencies.

6. **Verify the Installation of `git`**  
Command: `git --version`  
Output:  git version 2.34.1
- The user verifies the installation of `git` by checking its version.

7. **Install `vim`**  
Command: `sudo apt install -y vim`  
Output:  Reading package lists... Done Building dependency tree
Reading state information... Done The following additional packages will be installed: vim-common xxd
- The user installs `vim`, a text editor, alongside its dependencies.

8. **Verify the Installation of `vim`**  
Command: `vim --version`  
Output:  VIM - Vi IMproved 8.2
- The user verifies the installation of `vim` by checking its version.

9. **Clone the Official Git Repository**  
Command: `git clone https://github.com/git/git.git`  
Output:  Cloning into 'git'... remote: Enumerating objects: 3902, done. remote: Counting objects: 100% (3902/3902), done.
- The user clones the official Git repository from GitHub.

10. **Change Directory to the Cloned Repository**  
 Command: `cd git`  
 Output: None  
 - The user changes into the cloned repository directory.

11. **Build `git` from Source**  
 Command: `make prefix=/usr/local all`  
 Output:  
 ```
 make: Nothing to be done for 'all'.
 ```
 - The user attempts to build `git` but the repository was already built.

12. **Install the Built `git` Binaries**  
 Command: `sudo make prefix=/usr/local install`  
 Output:  
 ```
 install -m 755 git /usr/local/bin/git
 ```
 - The user installs the built `git` binaries to `/usr/local/bin/`.

13. **Verify the Installed Version of `git`**  
 Command: `git --version`  
 Output:  
 ```
 git version 2.34.1
 ```
 - The user verifies the installed version of `git`.

14. **Remove the `git` Package**  
 Command: `sudo apt remove -y git`  
 Output:  
 ```
 Reading package lists... Done
 Building dependency tree       
 Reading state information... Done
 The following packages will be REMOVED:
   git git-man
 ```
 - The user removes the `git` package that was installed through `apt`.

15. **Verify the Removal of `git`**  
 Command: `git --version`  
 Output:  
 ```
 git: 'git' is not installed. To install it, use:
     sudo apt install git
 ```
 - The user confirms that `git` has been successfully removed from the system.

16. **Exit the SSH Session**  
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
| `sudo apt upgrade -y`                  | Upgrade installed packages using `apt upgrade`.                                  |
| `sudo apt install -y git`              | Install `git` and its dependencies using `apt`.                                  |
| `git --version`                        | Verify the installation of `git`.                                                |
| `sudo apt install -y vim`              | Install `vim` and its dependencies using `apt`.                                  |
| `vim --version`                        | Verify the installation of `vim`.                                                |
| `git clone https://github.com/git/git.git`| Clone the official `git` repository from GitHub.                                |
| `cd git`                               | Change directory to the cloned `git` repository.                                |
| `make prefix=/usr/local all`           | Build `git` from source.                                                        |
| `sudo make prefix=/usr/local install`  | Install the built `git` binaries.                                                |
| `git --version`                        | Verify the installed version of `git`.                                           |
| `sudo apt remove -y git`               | Remove the `git` package using `apt remove`.                                      |
| `git --version`                        | Verify the successful removal of `git`.                                          |
| `exit`                                 | Exit the SSH session.                                                            |
