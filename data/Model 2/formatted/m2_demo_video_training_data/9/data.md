# Asciinema Recording Documentation: Deploying GNU Software on Debian Stable VM

This documentation provides a detailed overview of deploying a piece of GNU software on a Debian Stable virtual machine (VM). The software being deployed is the GNU Hello program, which outputs "Hello, world!" to the terminal. The process involves installing necessary build tools, downloading the software's source code, compiling, and installing it. Additionally, the VM is upgraded to Debian Unstable to obtain the latest package versions.

## Steps in the Recording

1. **Connect to Debian Stable VM via SSH**  
   Command: `ssh user@debian-stable-vm`  
   Output:  Welcome to Debian GNU/Linux 11 (bullseye)!
- The user connects to a Debian Stable VM using SSH.

2. **Check the Kernel Version**  
Command: `uname -r`  
Output:  5.10.0-19-amd64
- The user checks the kernel version of the Debian Stable system.

3. **Update Package Lists**  
Command: `sudo apt update`  
Output:  Get:1 http://deb.debian.org/debian stable InRelease [113 kB]
- The user updates the package lists to ensure they have the latest information on available packages.

4. **Install Build Essentials**  
Command: `sudo apt install -y build-essential`  
Output:  Reading package lists... Done Building dependency tree... Done Reading state information... Done

- The user installs the essential build tools needed for compiling software (`gcc`, `make`, etc.).

5. **Install Utilities (`wget`, `lynx`)**  
Command: `sudo apt install -y wget lynx`  
Output:  Reading package lists... Done Building dependency tree... Done Reading state information... Done
- The user installs `wget` and `lynx` for downloading and interacting with web resources.

6. **Download the GNU Hello Program**  
Command: `wget https://ftp.gnu.org/gnu/hello/hello-2.10.tar.gz`  
Output:  --2024-11-14 14:20:04-- https://ftp.gnu.org/gnu/hello/hello-2.10.tar.gz Resolving ftp.gnu.org (ftp.gnu.org)... 209.51.188.172
- The user downloads the GNU Hello program source code from the GNU FTP server.

7. **Extract the Source Code**  
Command: `tar -xvzf hello-2.10.tar.gz`  
Output:  hello-2.10/ hello-2.10/README hello-2.10/configure.ac
- The user extracts the contents of the `hello-2.10.tar.gz` archive using `tar`.

8. **Change Directory to the Extracted Folder**  
Command: `cd hello-2.10`  
Output: None  
- The user navigates to the extracted directory where the source code resides.

9. **Run the `configure` Script**  
Command: `./configure`  
Output:  checking for a working C compiler... yes checking for make... yes checking whether make sets $(MAKE)... yes
- The user runs the `configure` script to prepare the software for compilation.

10. **Compile the Software**  
 Command: `make`  
 Output:  
 ```
 gcc -DHAVE_CONFIG_H -I. -I. -g -O2 -MT hello.o -MD -MP -MF .deps/hello.Tpo -c hello.c
 gcc -g -O2 -o hello hello.o
 ```
 - The user compiles the source code using the `make` command.

11. **Install the Compiled Program**  
 Command: `sudo make install`  
 Output:  
 ```
 installing `hello` in /usr/local/bin
 ```
 - The user installs the compiled `hello` program into the system using `make install`.

12. **Run the Installed Program**  
 Command: `hello`  
 Output:  
 ```
 Hello, world!
 ```
 - The user runs the newly installed `hello` program to verify the installation.

13. **Check APT Sources**  
 Command: `cat /etc/apt/sources.list`  
 Output:  
 ```
 deb http://deb.debian.org/debian/ stable main contrib non-free
 deb-src http://deb.debian.org/debian/ stable main contrib non-free
 ```
 - The user checks the current sources list for Debian Stable repositories.

14. **Upgrade the System**  
 Command: `sudo apt upgrade`  
 Output:  
 ```
 Reading package lists... Done
 Building dependency tree... Done
 Reading state information... Done
 Calculating upgrade... Done
 The following packages will be upgraded:
 ```
 - The user upgrades the system to the latest packages available in the Debian Stable repositories.

15. **Install `hello` from Unstable Repository**  
 Command: `sudo apt install -t unstable hello`  
 Output:  
 ```
 Reading package lists... Done
 Building dependency tree... Done
 Reading state information... Done
 The following packages will be upgraded:
 ```
 - The user installs the `hello` package from the Unstable repository to ensure they have the latest version.

16. **Run the Upgraded Program**  
 Command: `hello`  
 Output:  
 ```
 Hello, world!
 ```
 - The user runs the upgraded `hello` program to verify that the upgrade was successful.

17. **Exit the Session**  
 Command: `exit`  
 Output: None  
 - The user ends the SSH session.

---

## Summary of Commands

| Command                             | Description                                                                 |
|-------------------------------------|-----------------------------------------------------------------------------|
| `ssh user@debian-stable-vm`         | Connect to a Debian Stable virtual machine via SSH.                         |
| `uname -r`                          | Check the kernel version of the Debian VM.                                  |
| `sudo apt update`                  | Update the package lists for the latest version of packages.                |
| `sudo apt install -y build-essential`| Install the essential build tools (`gcc`, `make`, etc.).                    |
| `sudo apt install -y wget lynx`     | Install utilities (`wget`, `lynx`) for downloading and interacting with web resources. |
| `wget https://ftp.gnu.org/gnu/hello/hello-2.10.tar.gz` | Download the GNU Hello program source code.                                  |
| `tar -xvzf hello-2.10.tar.gz`       | Extract the downloaded archive containing the GNU Hello source code.       |
| `cd hello-2.10`                     | Navigate to the extracted source code folder.                               |
| `./configure`                       | Prepare the source code for compilation.                                    |
| `make`                              | Compile the source code into the executable program.                        |
| `sudo make install`                 | Install the compiled program system-wide.                                   |
| `hello`                             | Run the installed GNU Hello program to verify installation.                 |
| `cat /etc/apt/sources.list`         | Check the package repositories in the sources list.                         |
| `sudo apt upgrade`                 | Upgrade the system to the latest available packages.                        |
| `sudo apt install -t unstable hello`| Install the latest version of `hello` from the Unstable repository.         |
| `exit`                              | End the SSH session.             
