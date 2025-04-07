# Asciinema Recording Documentation: Managing Files with `tar`

## Overview
This recording demonstrates creating a compressed archive with `tar`, extracting its contents, and ending the session.

---

## Timeline Breakdown

### 1. **Creating an Archive**
- **Command:** `tar -cvf archive.tar /folder`
- **Output:** `archive.tar`
- **Explanation:** The user creates a compressed archive (`archive.tar`) of the `/folder` directory.

### 2. **Checking Directory Contents**
- **Command:** `ls`
- **Output:** `archive.tar`
- **Explanation:** The user checks the contents of the directory, verifying that the archive is present.

### 3. **Extracting the Archive**
- **Command:** `tar -xvf archive.tar`
- **Output:** `folder/file1.txt folder/file2.txt`
- **Explanation:** The user extracts the contents of the `archive.tar` file. The system confirms the extraction.

### 4. **Ending the Session**
- **Command:** `exit`
- **Output:** *(none)*
- **Explanation:** The user exits the terminal session after managing the archive.

---

## Key Takeaways
- **File Archiving:** Demonstrated creating and extracting a compressed archive with `tar`.
- **Directory Verification:** Showcased checking the contents of the directory using `ls`.