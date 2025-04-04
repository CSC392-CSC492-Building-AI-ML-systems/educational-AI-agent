# Asciinema Recording Documentation: Deploying GNU `wget` on Fedora VM

This documentation covers the deployment and installation of the GNU `wget` program on a Fedora 38 virtual machine. The user encounters errors during the extraction and compilation process, which are resolved successfully. The session demonstrates how to handle common issues during software deployment on Fedora.

## Steps in the Recording

1. **Connect to Fedora VM via SSH**  
   Command: `ssh user@fedora-vm`  
   Output:  Welcome to Fedora 38 (Workstation Edition)!
- The user connects to a Fedora virtual machine via SSH.

2. **Check the Kernel Version**  
Command: `uname -r`  
Output:  6.1.0-0.fc38.x86_64
- The user checks the kernel version to ensure system compatibility.

3. **Update System Packages**  
Command: `sudo dnf update`  
Output:  Fedora 38 - x86_64 - Updates 2.3 MB/s | 25 MB 00:11
- The user updates the package lists for the latest package versions available in the Fedora repositories.

4. **Install Essential Tools**  
Command: `sudo dnf install -y wget curl gcc make`  
Output:  Dependencies resolved. Installation complete.
- The user installs essential utilities like `wget`, `curl`, `gcc`, and `make` on the Fedora system.

5. **Download the GNU `wget` Source Code**  
Command: `wget https://ftp.gnu.org/gnu/wget/wget-1.21.1.tar.gz`  
Output:  --2024-11-14 15:45:03-- https://ftp.gnu.org/gnu/wget/wget-1.21.1.tar.gz Resolving ftp.gnu.org (ftp.gnu.org)... 209.51.188.172
- The user downloads the `wget` program's source code from the GNU FTP server.

6. **Error During Extraction**  
Command: `tar -xvzf wget-1.21.1.tar.gz`  
Output:  tar: wget-1.21.1.tar.gz: Cannot open: No such file or directory tar: Error is not recoverable: exiting now
- An error occurs during extraction because the file is not found, likely due to a download issue.

7. **Verify File Presence**  
Command: `ls`  
Output:  tar: wget-1.21.1.tar.gz: Cannot open: No such file or directory tar: Error is not recoverable: exiting now
- An error occurs during extraction because the file is not found, likely due to a download issue.

7. **Verify File Presence**  
Command: `ls`  
Output:  wget-1.21.1.tar.gz
- The user verifies that the file `wget-1.21.1.tar.gz` is present in the directory.

8. **Retry Extraction**  
Command: `tar -xvzf wget-1.21.1.tar.gz`  
Output:  wget-1.21.1/ wget-1.21.1/README wget-1.21.1/configure.ac
- The extraction succeeds after confirming the file is correctly downloaded.

9. **Change to the Source Directory**  
Command: `cd wget-1.21.1`  
Output: None  
- The user navigates into the extracted directory of `wget` source code.

10. **Run the `configure` Script**  
 Command: `./configure`  
 Output:  
 ```
 checking for a working C compiler... yes
 checking for make... yes
 checking whether make sets $(MAKE)... yes
 ```
 - The `configure` script runs successfully, preparing the source code for compilation.

11. **Compilation Error Due to Invalid `-MT` Flag**  
 Command: `make`  
 Output:  
 ```
 gcc: error: unrecognized command line option ‘-MT’
 make: *** [Makefile:486: wget.o] Error 1
 ```
 - The compilation fails due to an unrecognized `-MT` flag in the Makefile.

12. **Clean Up the Build Environment**  
 Command: `make clean`  
 Output:  
 ```
 rm -f wget.o
 ```
 - The user cleans the build environment by removing partially compiled files.

13. **Fix the `Makefile`**  
 Command: `sed -i 's/-MT/-c/' Makefile`  
 Output: None  
 - The user modifies the `Makefile` to replace the invalid `-MT` flag with `-c`, correcting the build issue.

14. **Successful Compilation**  
 Command: `make`  
 Output:  
 ```
 gcc -DHAVE_CONFIG_H -I. -I. -g -O2 -c wget.c
 gcc -g -O2 -o wget wget.o
 ```
 - The program is successfully compiled after fixing the Makefile.

15. **Install the Program**  
 Command: `sudo make install`  
 Output:  
 ```
 installing `wget` in /usr/local/bin
 ```
 - The compiled `wget` program is installed system-wide on the Fedora VM.

16. **Verify Installation**  
 Command: `wget --version`  
 Output:  
 ```
 wget 1.21.1
 GNU Wget 1.21.1 built on linux-gnu.
 ```
 - The user verifies that the installed version of `wget` is correct by running `wget --version`.

17. **Exit the Session**  
 Command: `exit`  
 Output: None  
 - The user exits the SSH session after completing the installation of `wget`.

---

## Summary of Commands

| Command                               | Description                                                                 |
|---------------------------------------|-----------------------------------------------------------------------------|
| `ssh user@fedora-vm`                  | Connect to the Fedora virtual machine via SSH.                              |
| `uname -r`                            | Check the kernel version of the Fedora VM.                                  |
| `sudo dnf update`                    | Update the package lists for the latest versions of packages.               |
| `sudo dnf install -y wget curl gcc make`| Install essential utilities like `wget`, `curl`, `gcc`, and `make`.          |
| `wget https://ftp.gnu.org/gnu/wget/wget-1.21.1.tar.gz` | Download the source code for the GNU `wget` program.                         |
| `tar -xvzf wget-1.21.1.tar.gz`        | Extract the downloaded source code archive.                                 |
| `cd wget-1.21.1`                      | Change to the directory containing the extracted `wget` source code.        |
| `./configure`                         | Prepare the source code for compilation by running `configure`.             |
| `make`                                | Compile the source code into the executable program.                        |
| `sudo make install`                   | Install the compiled program system-wide.                                   |
| `wget --version`                      | Verify the installation by checking the version of `wget`.                  |
| `exit`                                | End the SSH session.                                                       |

This session demonstrates how to deploy the GNU `wget` program on a Fedora VM, troubleshooting errors encountered during extraction and compilation. The installation is completed successfully, and the user verifies the program's functionality.
