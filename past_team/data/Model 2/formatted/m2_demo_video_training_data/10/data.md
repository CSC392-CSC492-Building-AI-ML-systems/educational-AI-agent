# Asciinema Recording Documentation: Deploying GNU Software on Debian Stable VM (with Errors Encountered)

This documentation outlines the process of deploying a piece of GNU software (GNU Hello) on a Debian Stable virtual machine (VM). The user encounters some errors during the process, including issues with file extraction and compilation, which are then resolved. Additionally, the VM is upgraded to Debian Unstable to ensure the installation of the latest software versions.

## Steps in the Recording

1. **Connect to Debian Stable VM via SSH**  
   Command: `ssh user@debian-stable-vm`  
   Output:  Welcome to Debian GNU/Linux 11 (bullseye)!
- The user connects to a Debian Stable VM via SSH.

2. **Check the Kernel Version**  
Command: `uname -r`  
Output:  5.10.0-19-amd64
- The user checks the kernel version to ensure compatibility.

3. **Update Package Lists**  
Command: `sudo apt update`  
Output:  Get:1 http://deb.debian.org/debian stable InRelease [113 kB]
- The package list is updated to reflect the latest versions in the Debian Stable repositories.

4. **Install Essential Build Tools**  
Command: `sudo apt install -y build-essential`  
Output:  Reading package lists... Done Building dependency tree... Done Reading state information... Done
- The user installs essential development tools like `gcc`, `make`, and others needed to build GNU software.

5. **Install Utilities (`wget`, `lynx`)**  
Command: `sudo apt install -y wget lynx`  
Output:  Reading package lists... Done Building dependency tree... Done Reading state information... Done
- The user installs utilities such as `wget` and `lynx` for downloading and interacting with web resources.

6. **Download the GNU Hello Program**  
Command: `wget https://ftp.gnu.org/gnu/hello/hello-2.10.tar.gz`  
Output:  --2024-11-14 14:20:04-- https://ftp.gnu.org/gnu/hello/hello-2.10.tar.gz Resolving ftp.gnu.org (ftp.gnu.org)... 209.51.188.172
- The user downloads the latest version of the GNU Hello program from the FTP server.

7. **Error in Extracting the Archive**  
Command: `tar -xvzf hello-2.10.tar.gz`  
Output:  tar (child): hello-2.10.tar.gz: Cannot open: No such file or directory tar (child): Error is not recoverable: exiting now tar: Child returned status 2 tar: Error is not recoverable: exiting now
- An error occurs because the file is not found, possibly due to a typo or the file not being downloaded correctly.

8. **Check for the Presence of the File**  
Command: `ls`  
Output:  hello-2.10.tar.gz
- The user checks the directory contents and verifies that the file is present.

9. **Retry Extraction**  
Command: `tar -xvzf hello-2.10.tar.gz`  
Output:  hello-2.10/ hello-2.10/README hello-2.10/configure.ac
- After confirming the file is present, the user successfully extracts the archive.

10. **Navigate to the Source Directory**  
 Command: `cd hello-2.10`  
 Output: None  
 - The user changes the directory to the extracted source folder.

11. **Run the `configure` Script**  
 Command: `./configure`  
 Output:  
 ```
 checking for a working C compiler... yes
 checking for make... yes
 checking whether make sets $(MAKE)... yes
 ```
 - The `configure` script successfully prepares the source for compilation.

12. **Compilation Error Due to Invalid Compiler Flag**  
 Command: `make`  
 Output:  
 ```
 gcc: error: unrecognized command line option ‘-MT’
 make: *** [Makefile:486: hello.o] Error 1
 ```
 - Compilation fails because of an unrecognized `-MT` option in the Makefile.

13. **Clean Up Before Retrying**  
 Command: `make clean`  
 Output:  
 ```
 rm -f hello.o
 ```
 - The user cleans up the compiled files before attempting the build again.

14. **Fix the Makefile**  
 Command: `sed -i 's/-MT/-c/' Makefile`  
 Output: None  
 - The user modifies the Makefile to replace the incorrect `-MT` flag with `-c` to resolve the compiler error.

15. **Successful Compilation**  
 Command: `make`  
 Output:  
 ```
 gcc -DHAVE_CONFIG_H -I. -I. -g -O2 -c hello.c
 gcc -g -O2 -o hello hello.o
 ```
 - The user successfully compiles the program after fixing the Makefile.

16. **Install the Program**  
 Command: `sudo make install`  
 Output:  
 ```
 installing `hello` in /usr/local/bin
 ```
 - The compiled program is installed system-wide.

17. **Run the Installed Program**  
 Command: `hello`  
 Output:  
 ```
 Hello, world!
 ```
 - The user runs the newly installed `hello` program, which outputs the expected message.

18. **Check Package Sources**  
 Command: `cat /etc/apt/sources.list`  
 Output:  
 ```
 deb http://deb.debian.org/debian/ stable main contrib non-free
 deb-src http://deb.debian.org/debian/ stable main contrib non-free
 ```
 - The user checks the package repositories to confirm the current setup.

19. **Upgrade System**  
 Command: `sudo apt upgrade`  
 Output:  
 ```
 Reading package lists... Done
 Building dependency tree... Done
 Reading state information... Done
 Calculating upgrade... Done
 The following packages will be upgraded:
 ```
 - The system is upgraded to the latest available packages from Debian Stable.

20. **Install `hello` from Unstable Repository**  
 Command: `sudo apt install -t unstable hello`  
 Output:  
 ```
 Reading package lists... Done
 Building dependency tree... Done
 Reading state information... Done
 The following packages will be upgraded:
 ```
 - The user installs the latest version of `hello` from the Unstable repository.

21. **Run the Upgraded Program**  
 Command: `hello`  
 Output:  
 ```
 Hello, world!
 ```
 - The upgraded version of the `hello` program is executed successfully.

22. **End the Session**  
 Command: `exit`  
 Output: None  
 - The user exits the SSH session after completing the task.

---

## Summary of Commands

| Command                             | Description                                                                 |
|-------------------------------------|-----------------------------------------------------------------------------|
| `ssh user@debian-stable-vm`         | Connect to the Debian Stable virtual machine via SSH.                       |
| `uname -r`                          | Check the kernel version of the Debian VM.                                  |
| `sudo apt update`                  | Update the package lists for the latest versions of packages.               |
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
| `exit`                              | End the SSH session.                                                       |

This session walks through the process of deploying and upgrading GNU software on a Debian Stable VM, troubleshooting errors encountered during the installation, and ensuring that the latest version of `hello` is installed from the Unstable repository.
