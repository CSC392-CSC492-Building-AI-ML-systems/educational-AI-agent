# Asciinema Recording Documentation

This documentation summarizes a terminal session demonstrating basic Git and file management operations. Below is a detailed breakdown of each step.

## Steps in the Recording

1. **Display Current Directory**  
   Command: `pwd`  
   Output: `/home/user`  
   - The `pwd` command displays the current working directory.

2. **List All Files (Including Hidden)**  
   Command: `ls -a`  
   Output: `.. .bashrc file1.txt file2.txt project/`
- The `ls -a` command lists all files, including hidden ones, in the current directory.

3. **Change Directory**  
Command: `cd project`  
Output: None  
- Changes the working directory to the `project` folder.

4. **Check Git Repository Status**  
Command: `git status`  
Output: `On branch main\nNo commits yet\nUntracked files:\n(use "git add <file>..." to include in what will be committed)\nnew_file.txt\nnothing added to commit but untracked files present (use "git add" to track)`
- Shows the status of the Git repository, including untracked files and the current branch.

5. **Create a File with Initial Content**  
Command: `echo "Initial content" > new_file.txt`  
Output: None  
- Writes the string "Initial content" to `new_file.txt`, overwriting any existing content.

6. **Stage a File for Commit**  
Command: `git add new_file.txt`  
Output: None  
- Stages `new_file.txt` for the next commit.

7. **Commit Changes to Git**  
Command: `git commit -m "Add new_file.txt with initial content"`  
Output:  `[main (root-commit) abc1234] Add new_file.txt with initial content 1 file changed, 1 insertion(+) create mode 100644 new_file.txt`

- Creates a commit with the staged changes and a message describing the changes.

8. **View Commit Log**  
Command: `git log --oneline`  
Output:  `abc1234 (HEAD -> main) Add new_file.txt with initial content`
- Shows a concise log of commits in the repository.

9. **Delete a File**  
Command: `rm new_file.txt`  
Output: None  
- Deletes `new_file.txt` from the current directory.

10. **Check Git Repository Status Again**  
 Command: `git status`  
 Output:  
 ```
 On branch main  
 Changes not staged for commit:  
   (use "git add/rm <file>..." to update what will be committed)  
   (use "git restore <file>..." to discard changes in working directory)  
   deleted: new_file.txt  
 no changes added to commit (use "git add" and/or "git commit -a")
 ```
 - Confirms that `new_file.txt` has been deleted and the deletion is unstaged.

11. **End the Session**  
 Command: `exit`  
 Output: None  
 - Ends the terminal session.

---

## Summary of Commands

| Command                    | Description                                                                                  |
|----------------------------|----------------------------------------------------------------------------------------------|
| `pwd`                      | Displays the current working directory.                                                     |
| `ls -a`                    | Lists all files, including hidden files, in the current directory.                          |
| `cd <directory>`           | Changes the current working directory to the specified folder.                              |
| `git status`               | Displays the status of the Git repository, showing changes and staged files.                |
| `echo "text" > <file>`     | Writes the specified text to a file, overwriting any existing content.                      |
| `git add <file>`           | Stages the specified file for the next commit.                                              |
| `git commit -m "message"`  | Creates a commit with staged changes and a descriptive message.                             |
| `git log --oneline`        | Shows a concise log of commits in the repository.                                           |
| `rm <file>`                | Deletes the specified file.                                                                 |
| `exit`                     | Ends the terminal session.                                                                  |

This session provides an overview of fundamental file manipulation and version control using Git in a Unix-based shell environment.





