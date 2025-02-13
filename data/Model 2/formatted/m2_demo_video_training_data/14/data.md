# Asciinema Recording Documentation: System Monitoring in Fedora

This documentation describes a session where the user performs system monitoring tasks in a Fedora virtual machine (VM). The operations include connecting to the VM, updating the system, installing software, and checking system processes using `htop`.

## Steps in the Recording

1. **Connect to Fedora VM via SSH**  
   Command: `ssh user@fedora-vm`  
   Output:  Welcome to Fedora 38
- The user connects to the Fedora virtual machine via SSH.

2. **Check the Kernel Version**  
Command: `uname -r`  
Output:  6.3.8-200.fc38.x86_64
- The user checks the kernel version of the Fedora VM to verify the system environment.

3. **Update System Packages**  
Command: `sudo dnf update -y`  
Output:  ...updating system...
- The user updates all system packages to the latest versions using the `dnf` package manager.

4. **Install `htop` System Monitor**  
Command: `sudo dnf install htop`  
Output:  Installing package htop...
- The user installs `htop`, a system monitor tool for viewing processes and system resources.

5. **Launch `htop` to View System Processes**  
Command: `htop`  
Output:  ...output showing system processes...
- The user launches `htop` to display the running processes, CPU usage, memory usage, and other system statistics.

6. **Exit the Fedora VM**  
Command: `exit`  
Output: None  
- The user exits the SSH session after completing the system monitoring tasks.

---

## Summary of Commands

| Command                               | Description                                                                |
|---------------------------------------|----------------------------------------------------------------------------|
| `ssh user@fedora-vm`                  | Connect to the Fedora virtual machine via SSH.                             |
| `uname -r`                            | Check the kernel version of the Fedora VM.                                 |
| `sudo dnf update -y`                  | Update all system packages to the latest versions using `dnf` package manager. |
| `sudo dnf install htop`               | Install `htop`, a system monitor tool for viewing system processes.        |
| `htop`                                | Launch `htop` to view running processes and system resources.              |
| `exit`                                | Exit the SSH session after completing the tasks.                           |

In this session, the user successfully connects to a Fedora VM, updates the system, installs the `htop` system monitor tool, views system processes, and exits the session.
