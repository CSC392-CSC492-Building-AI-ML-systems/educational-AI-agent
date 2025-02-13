# Asciinema Recording Documentation: File Operations in Ubuntu

This documentation describes a session where the user performs basic file operations in an Ubuntu VM. These operations include creating files, writing content to them, moving files between directories, and removing files.

## Steps in the Recording

1. **Connect to Ubuntu VM via SSH**  
   Command: `ssh user@ubuntu-vm`  
   Output:  Welcome to Ubuntu 24.04 LTS
- The user connects to the Ubuntu virtual machine via SSH.

2. **Check the Kernel Version**  
Command: `uname -r`  
Output:  6.2.0-26-generic
- The user checks the kernel version of the Ubuntu VM to verify the system environment.

3. **Create a New Directory for the Project**  
Command: `mkdir ~/project`  
Output: None  
- A new directory called `project` is created in the user's home directory.

4. **Change to the Project Directory**  
Command: `cd ~/project`  
Output: None  
- The user navigates into the `project` directory where they will perform file operations.

5. **Create Two Text Files**  
Command: `touch file1.txt file2.txt`  
Output: None  
- The user creates two new text files, `file1.txt` and `file2.txt`, inside the `project` directory.

6. **Verify the Files**  
Command: `ls`  
Output:  6.2.0-26-generic
- The user checks the kernel version of the Ubuntu VM to verify the system environment.

3. **Create a New Directory for the Project**  
Command: `mkdir ~/project`  
Output: None  
- A new directory called `project` is created in the user's home directory.

4. **Change to the Project Directory**  
Command: `cd ~/project`  
Output: None  
- The user navigates into the `project` directory where they will perform file operations.

5. **Create Two Text Files**  
Command: `touch file1.txt file2.txt`  
Output: None  
- The user creates two new text files, `file1.txt` and `file2.txt`, inside the `project` directory.

6. **Verify the Files**  
Command: `ls`  
Output:  file1.txt file2.txt
- The user lists the contents of the `project` directory to confirm the creation of the files.

7. **Write to `file1.txt`**  
Command: `echo "Hello World" > file1.txt`  
Output: None  
- The user writes the string "Hello World" to `file1.txt` using output redirection.

8. **Display the Contents of `file1.txt`**  
Command: `cat file1.txt`  
Output:  Hello World
- The user displays the contents of `file1.txt` to verify the content was written correctly.

9. **Write to `file2.txt`**  
Command: `echo "This is file 2" > file2.txt`  
Output: None  
- The user writes the string "This is file 2" to `file2.txt`.

10. **Display the Contents of `file2.txt`**  
 Command: `cat file2.txt`  
 Output:  
 ```
 This is file 2
 ```
 - The user displays the contents of `file2.txt` to verify the content was written correctly.

11. **Move `file1.txt` to the Documents Directory**  
 Command: `mv file1.txt ~/Documents/`  
 Output: None  
 - The user moves `file1.txt` to the `Documents` directory.

12. **Verify the Project Directory**  
 Command: `ls`  
 Output:  
 ```
 file2.txt
 ```
 - The user lists the contents of the `project` directory to confirm that `file1.txt` has been moved.

13. **Verify the Documents Directory**  
 Command: `ls ~/Documents`  
 Output:  
 ```
 file1.txt
 ```
 - The user verifies that `file1.txt` is now located in the `Documents` directory.

14. **Remove `file2.txt` from the Project Directory**  
 Command: `rm file2.txt`  
 Output: None  
 - The user removes `file2.txt` from the `project` directory.

15. **Verify the Project Directory After Deletion**  
 Command: `ls`  
 Output: None  
 - The user verifies that `file2.txt` has been deleted from the `project` directory.

16. **Exit the SSH Session**  
 Command: `exit`  
 Output: None  
 - The user exits the SSH session after completing the file operations.

---

## Summary of Commands

| Command                              | Description                                                                 |
|--------------------------------------|-----------------------------------------------------------------------------|
| `ssh user@ubuntu-vm`                 | Connect to the Ubuntu virtual machine via SSH.                              |
| `uname -r`                           | Check the kernel version of the Ubuntu VM.                                  |
| `mkdir ~/project`                    | Create a new directory called `project` in the user's home directory.       |
| `cd ~/project`                       | Navigate into the `project` directory.                                      |
| `touch file1.txt file2.txt`          | Create two new text files, `file1.txt` and `file2.txt`.                     |
| `ls`                                 | List the contents of the current directory to verify the files.             |
| `echo "Hello World" > file1.txt`     | Write "Hello World" to `file1.txt` using output redirection.                |
| `cat file1.txt`                      | Display the contents of `file1.txt`.                                        |
| `echo "This is file 2" > file2.txt`  | Write "This is file 2" to `file2.txt` using output redirection.             |
| `cat file2.txt`                      | Display the contents of `file2.txt`.                                        |
| `mv file1.txt ~/Documents/`          | Move `file1.txt` to the `Documents` directory.                              |
| `ls`                                 | Verify the contents of the `project` directory after moving the file.       |
| `ls ~/Documents`                     | Verify that `file1.txt` is now located in the `Documents` directory.        |
| `rm file2.txt`                       | Remove `file2.txt` from the `project` directory.                            |
| `ls`                                 | Verify the contents of the `project` directory after deleting the file.     |
| `exit`                               | End the SSH session.                                                       |

This session demonstrates common file operations in a Linux environment, such as creating files, writing content, moving files between directories, and deleting files. The user successfully navigates through these tasks within an Ubuntu virtual machine.
